import abc
from typing import List

import inject
from tic_tac_toe.domain import exceptions
from tic_tac_toe.domain.entities import Board
from tic_tac_toe.domain.entities import GameSession
from tic_tac_toe.domain.entities import GameSessionTurn
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.entities import TicTacToeGame
from tic_tac_toe.domain.object_values import CROSS
from tic_tac_toe.domain.object_values import GameSessionStatus
from tic_tac_toe.domain.object_values import NOUGHT
from tic_tac_toe.domain.object_values import PlayerAction
from tic_tac_toe.domain.object_values import UserSession
from tic_tac_toe.domain.repositories import IGameRepository
from tic_tac_toe.domain.repositories import IPlayerRepository


class Service(abc.ABC):
    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass


class CreateGameService(Service):
    def execute(self, *args, **kwargs):
        pass


class CreatePlayerService(Service):
    _player_repository = inject.instance(IPlayerRepository)

    def execute(self, player: Player) -> Player:
        current_player = self._player_repository.get_by_name(name=player.name)

        if current_player:
            raise exceptions.PlayerAlreadyExistsException()

        player = self._player_repository.save(player)

        return player


class AuthenticatePlayer(Service):
    _player_repository = inject.instance(IPlayerRepository)

    def execute(self, player: Player) -> UserSession:
        authenticated_player = self._player_repository.auth(player)

        if not authenticated_player:
            raise exceptions.PlayerUnAuthorizedException()

        user_session = self._player_repository.get_user_session(player)

        return user_session


class GetGameSessionService(Service):
    _game_repository = inject.instance(IGameRepository)

    def execute(self, game_session_id: str) -> GameSession:
        game_session = self._game_repository.get_session(game_session_id)

        if not game_session:
            raise exceptions.InvalidGameSessionException()

        return game_session


class ValidateUserSessionService(Service):
    _player_repository = inject.instance(IPlayerRepository)

    def execute(self, user_session: UserSession) -> Player:
        player = self._player_repository.validate_user_session(user_session)

        if not player:
            raise exceptions.InvalidUserSessionException()

        return player


class ClosePlayerOpenGameSessionService(Service):
    _game_repository = inject.instance(IGameRepository)

    def execute(self, player_name) -> List[GameSession]:
        open_sessions = self._game_repository.list_open_player_sessions(player_name)
        for session in open_sessions:
            self._game_repository.close_session(session)

        return open_sessions


class StartTicTacToeGameService(Service):
    _game_repository = inject.instance(IGameRepository)
    _close_player_open_game_sessions_srv = inject.instance(
        ClosePlayerOpenGameSessionService
    )

    def execute(self, player_name) -> GameSession:
        self._close_player_open_game_sessions_srv.execute(player_name)

        game = TicTacToeGame()

        player = Player(name=player_name, is_host=True, item=CROSS)

        game_session = GameSession(game=game, players=[player], host=player_name)

        self._game_repository.save_session(game_session)

        return game_session


class CheckGameSessionBoardService(Service):
    def execute(self, board: Board):
        for vector in board.get_vector():
            if all(item == vector[0] for item in vector):
                return vector[0]

        return False


class ResolveGameSessionStatusService(Service):
    _check_game_session_board_srv = inject.instance(CheckGameSessionBoardService)

    def execute(self, turn: GameSessionTurn) -> GameSessionTurn:
        completed_vector_item = self._check_game_session_board_srv.execute(
            turn.game_session.game.board
        )
        if completed_vector_item:
            turn.game_session.winner = turn.player.name
            turn.change_to_status = GameSessionStatus.OVER
            turn.change_status_reason = f"{turn.player.name} wins!"

        if turn.game_session.game.board.is_full():
            turn.change_to_status = GameSessionStatus.OVER
            turn.change_status_reason = "Draw!"

        if turn.change_to_status:
            turn.game_session.status = turn.change_to_status
        return turn


class ConnectToGameService(Service):
    def execute(self, turn: GameSessionTurn) -> GameSessionTurn:
        turn.change_to_status = GameSessionStatus.WAITING_FOR_HOST_APPROVAL
        return turn


class ResumeGameService(Service):
    def execute(self, turn: GameSessionTurn) -> GameSessionTurn:
        return turn


class AdmitPlayerService(Service):
    def execute(self, turn: GameSessionTurn) -> GameSessionTurn:
        if not turn.player.is_host:
            raise exceptions.ActionNotAllowedException()

        turn.change_to_status = GameSessionStatus.RUNNING

        player = Player(name=turn.player_name, item=NOUGHT)
        turn.game_session.add_player(player)

        return turn


class MarkItemOnBoardService(Service):
    def execute(self, turn: GameSessionTurn) -> GameSessionTurn:
        game = turn.game_session.game

        if game.board.points[turn.position.x][turn.position.y] is not None:
            raise exceptions.PositionAlreadyMarkedException()

        game.board.points[turn.position.x][turn.position.y] = turn.item

        turn.game_session.set_next_turn()

        return turn


class PlayGameService(Service):
    _game_repository = inject.instance(IGameRepository)
    _connect_to_game_srv = inject.instance(ConnectToGameService)
    _admit_player_srv = inject.instance(AdmitPlayerService)
    _resolve_game_session_status_srv = inject.instance(ResolveGameSessionStatusService)
    _mark_item_on_board_srv = inject.instance(MarkItemOnBoardService)
    _resume_game_srv = inject.instance(ResumeGameService)

    def execute(self, turn: GameSessionTurn) -> GameSessionTurn:
        game_session = self._game_repository.get_session(turn.game_session_id)

        if not game_session:
            raise exceptions.InvalidGameSessionException()

        turn.game_session = game_session

        self._validate_player_turn(turn)
        self._validate_position(turn)

        action_service = self._get_service_by_action(turn.action, game_session.status)

        if not action_service:
            raise exceptions.InvalidActionException()

        action_turn = action_service.execute(turn)

        next_turn = self._resolve_game_session_status_srv.execute(action_turn)

        self._game_repository.update_session(next_turn.game_session)

        return next_turn

    def _get_service_by_action(self, action: PlayerAction, status: GameSessionStatus):
        _service_by_action_map = {
            (
                PlayerAction.CONNECT,
                GameSessionStatus.WAITING_FOR_PLAYER,
            ): self._connect_to_game_srv,
            (
                PlayerAction.CONNECT,
                GameSessionStatus.WAITING_FOR_HOST_APPROVAL,
            ): self._connect_to_game_srv,
            (
                PlayerAction.ADMIT_PLAYER,
                GameSessionStatus.WAITING_FOR_HOST_APPROVAL,
            ): self._admit_player_srv,
            (
                PlayerAction.MARK,
                GameSessionStatus.RUNNING,
            ): self._mark_item_on_board_srv,
            (
                PlayerAction.RESUME,
                GameSessionStatus.RUNNING,
            ): self._resume_game_srv,
            (
                PlayerAction.RESUME,
                GameSessionStatus.OVER,
            ): self._resume_game_srv,
        }

        return _service_by_action_map.get((action, status))

    def _validate_player_turn(self, turn: GameSessionTurn):
        next_turn_player = turn.game_session.next_turn_player

        if (
            turn.game_session.status == GameSessionStatus.RUNNING
            and turn.action != PlayerAction.RESUME
            and turn.player.name != next_turn_player.name
        ):
            raise exceptions.ActionNotAllowedException()

        for player in turn.game_session.players:
            if player.name == turn.player.name:
                if turn.item and player.item != turn.item:
                    raise exceptions.InvalidPlayerItemException()

                turn.player.is_host = player.is_host

    def _validate_position(self, turn):
        board_size = turn.game_session.game.board.size
        max_x_pos = board_size[0] - 1
        max_y_pos = board_size[1] - 1

        if turn.position and (
            turn.position.x > max_x_pos or turn.position.y > max_y_pos
        ):
            raise exceptions.PositionOutOfBoardException()


class ListOpenGameSessionsService(Service):
    _game_repository = inject.instance(IGameRepository)

    def execute(self, player_name: str) -> list:
        open_sessions = self._game_repository.list_open_sessions(limit=5)

        open_sessions_for_player = []
        for session in open_sessions:
            if session.host != player_name:
                open_sessions_for_player.append(session)

        return open_sessions_for_player


class ListOverPlayerSessionsService(Service):
    _game_repository = inject.instance(IGameRepository)

    def execute(self, player_name: str) -> list:
        sessions = self._game_repository.list_over_player_sessions(player_name)

        return sessions
