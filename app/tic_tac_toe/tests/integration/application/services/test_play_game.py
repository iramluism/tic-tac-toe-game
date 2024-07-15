from unittest.mock import Mock

import inject
import pytest
from tic_tac_toe.domain.entities import GameSession
from tic_tac_toe.domain.entities import GameSessionTurn
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.entities import TicTacToeGame
from tic_tac_toe.domain.exceptions import InvalidActionException
from tic_tac_toe.domain.exceptions import PositionOutOfBoardException
from tic_tac_toe.domain.object_values import CROSS
from tic_tac_toe.domain.object_values import GameSessionStatus
from tic_tac_toe.domain.object_values import NOUGHT
from tic_tac_toe.domain.object_values import PlayerAction
from tic_tac_toe.domain.repositories import IGameRepository


@pytest.fixture
def play_game_service():
    inject.configure_once()
    from tic_tac_toe.application.services import PlayGameService

    return PlayGameService()


def test_change_to_waiting_for_approval_status_when_connecting_to_game(
    play_game_service,
):
    # Arrange
    game = TicTacToeGame()
    game_session = GameSession(
        game=game,
        status=GameSessionStatus.WAITING_FOR_PLAYER,
        host="player-1",
        players=[Player(name="player-1")],
        is_over=False,
    )

    mock_game_repository = Mock(spec=IGameRepository)
    mock_game_repository.get_session.return_value = game_session

    play_game_service._game_repository = mock_game_repository

    guest_player = Player(name="player-2")

    turn = GameSessionTurn(
        game_session_id=game_session.id,
        action=PlayerAction.CONNECT,
        player=guest_player,
        player_name=guest_player.name,
    )

    # Act
    turn = play_game_service.execute(turn)

    # Assert
    assert turn.game_session.status == GameSessionStatus.WAITING_FOR_HOST_APPROVAL


def test_change_to_running_status_after_approve_host(play_game_service):
    # Arrange
    game = TicTacToeGame()
    host_player = Player(name="player-1", is_host=True)
    game_session = GameSession(
        game=game,
        status=GameSessionStatus.WAITING_FOR_HOST_APPROVAL,
        host="player-1",
        players=[host_player],
        is_over=False,
    )

    mock_game_repository = Mock(spec=IGameRepository)
    mock_game_repository.get_session.return_value = game_session

    play_game_service._game_repository = mock_game_repository

    guest_player = Player(name="player-2")
    turn = GameSessionTurn(
        game_session_id=game_session.id,
        action=PlayerAction.ADMIT_PLAYER,
        player=host_player,
        player_name=guest_player.name,
    )

    # Act
    turn = play_game_service.execute(turn)

    # Assert
    assert turn.game_session.status == GameSessionStatus.RUNNING
    assert guest_player.name in [player.name for player in turn.game_session.players]
    assert len(turn.game_session.players) == 2


HOST_PLAYER = Player(name="player-1", is_host=True, item=CROSS)
GUEST_PLAYER = Player(name="player-2", item=NOUGHT)

GAME = TicTacToeGame()
GAME_SESSION = GameSession(
    game=GAME,
    status=GameSessionStatus.RUNNING,
    host=HOST_PLAYER.name,
    players=[HOST_PLAYER, GUEST_PLAYER],
    is_over=False,
)


@pytest.mark.parametrize(
    "points,item,turn_player,guest_player,host_player,position,expected_points,expected_status,expected_winner",  # noqa
    [
        (
            [[None, None, None], [None, None, None], [None, None, None]],
            CROSS,
            HOST_PLAYER,
            GUEST_PLAYER,
            HOST_PLAYER,
            (0, 0),
            [[CROSS, None, None], [None, None, None], [None, None, None]],
            GameSessionStatus.RUNNING,
            None,
        ),
        (
            [[CROSS, NOUGHT, None], [CROSS, None, None], [None, NOUGHT, None]],
            CROSS,
            HOST_PLAYER,
            GUEST_PLAYER,
            HOST_PLAYER,
            (2, 0),
            [[CROSS, NOUGHT, None], [CROSS, None, None], [CROSS, NOUGHT, None]],
            GameSessionStatus.OVER,
            HOST_PLAYER.name,
        ),
    ],
)
def test_mark_item_on_board(
    points,
    item,
    turn_player,
    guest_player,
    host_player,
    position,
    expected_points,
    expected_status,
    expected_winner,
    play_game_service,
):
    # Arrange
    game = TicTacToeGame()
    game.board.points = points
    game_session = GameSession(
        game=game,
        status=GameSessionStatus.RUNNING,
        host=host_player.name,
        players=[host_player, guest_player],
        is_over=False,
    )

    mock_game_repository = Mock(spec=IGameRepository)
    mock_game_repository.get_session.return_value = game_session

    play_game_service._game_repository = mock_game_repository

    turn = GameSessionTurn(
        game_session_id=game_session.id,
        action=PlayerAction.MARK,
        player=turn_player,
        item=item,
        position=position,
    )

    # Act
    turn = play_game_service.execute(turn)

    # Assert
    assert expected_points == turn.game_session.game.board.points
    assert expected_status == turn.game_session.status
    assert expected_winner == turn.game_session.winner


def test_resume_game(play_game_service):
    # Arrange
    game = TicTacToeGame()
    game_session = GameSession(
        game=game,
        status=GameSessionStatus.RUNNING,
        host="player-1",
        players=[Player(name="player-1")],
        is_over=False,
    )

    mock_game_repository = Mock(spec=IGameRepository)
    mock_game_repository.get_session.return_value = game_session

    play_game_service._game_repository = mock_game_repository

    guest_player = Player(name="player-2")

    turn = GameSessionTurn(
        game_session_id=game_session.id,
        action=PlayerAction.RESUME,
        player=guest_player,
        player_name=guest_player.name,
    )

    # Act
    turn = play_game_service.execute(turn)

    # Assert
    assert turn.game_session == game_session


@pytest.mark.parametrize(
    "turn,game_session",
    [
        # connect to game in not waiting for player status
        (
            GameSessionTurn(
                game_session_id="fake-game-session-id",
                action=PlayerAction.RESUME,
                player=GUEST_PLAYER,
                player_name=GUEST_PLAYER.name,
            ),
            GameSession(
                game=TicTacToeGame(),
                status=GameSessionStatus.WAITING_FOR_PLAYER,
                host=HOST_PLAYER.name,
                players=[HOST_PLAYER],
                is_over=False,
            ),
        ),
        # admit user in not waiting for host approval status
        (
            GameSessionTurn(
                game_session_id="fake-game-session-id",
                action=PlayerAction.ADMIT_PLAYER,
                player=HOST_PLAYER,
                player_name=GUEST_PLAYER.name,
            ),
            GameSession(
                game=TicTacToeGame(),
                status=GameSessionStatus.WAITING_FOR_PLAYER,
                host=HOST_PLAYER.name,
                players=[HOST_PLAYER],
                is_over=False,
            ),
        ),
        # mark item in not running status
        (
            GameSessionTurn(
                game_session_id="fake-game-session-id",
                action=PlayerAction.MARK,
                player=HOST_PLAYER,
                player_name=GUEST_PLAYER.name,
            ),
            GameSession(
                game=TicTacToeGame(),
                status=GameSessionStatus.WAITING_FOR_PLAYER,
                host=HOST_PLAYER.name,
                players=[HOST_PLAYER],
                is_over=False,
            ),
        ),
        (
            GameSessionTurn(
                game_session_id="fake-game-session-id",
                action=PlayerAction.MARK,
                player=HOST_PLAYER,
                player_name=GUEST_PLAYER.name,
            ),
            GameSession(
                game=TicTacToeGame(),
                status=GameSessionStatus.WAITING_FOR_PLAYER,
                host=HOST_PLAYER.name,
                players=[HOST_PLAYER],
                is_over=False,
            ),
        ),
    ],
)
def test_raise_invalid_action(play_game_service, turn, game_session):
    play_game_service._game_repository = Mock(spec=IGameRepository)
    play_game_service._game_repository.get_session.return_value = game_session

    with pytest.raises(InvalidActionException):
        play_game_service.execute(turn)


def test_raise_error_if_position_is_out_of_board(play_game_service):
    game_session = GAME_SESSION
    game_session.status = GameSessionStatus.RUNNING
    game_session.next_turn = 1  # guest player turn

    mock_game_repository = Mock(spec=IGameRepository)
    mock_game_repository.get_session.return_value = game_session

    play_game_service._game_repository = mock_game_repository

    turn = GameSessionTurn(
        game_session_id=game_session.id,
        action=PlayerAction.MARK,
        player=GUEST_PLAYER,
        item=NOUGHT,
        position=(3, 3),  # out of board
    )

    # Act
    with pytest.raises(PositionOutOfBoardException):
        play_game_service.execute(turn)
