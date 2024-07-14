import json
from typing import List
from typing import Optional

from django.db.models import Q
from tic_tac_toe.domain.entities import Board
from tic_tac_toe.domain.entities import Game
from tic_tac_toe.domain.entities import GameSession
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.object_values import GameSessionStatus
from tic_tac_toe.domain.repositories import IGameRepository
from tic_tac_toe.infrastructure.repositories import models


class GameRepository(IGameRepository):
    def save(self, game):
        pass

    def get(self, game_id):
        pass

    def list_open_sessions(self, limit: Optional[int] = None):
        db_game_sessions = models.GameSession.objects.filter(
            status=GameSessionStatus.WAITING_FOR_PLAYER.value
        )

        if limit:
            db_game_sessions = db_game_sessions[:limit]

        game_sessions = []
        for db_game_session in db_game_sessions:
            db_players = models.GameSessionPlayer.objects.filter(
                Q(game_session_id=db_game_session.id)
            )

            game_session = self._map_to_game_session_entity(db_game_session, db_players)
            game_sessions.append(game_session)

        return game_sessions

    def update_session(self, game_session: GameSession) -> GameSession:
        queryset = models.GameSession.objects.filter(id=game_session.id)

        if not queryset:
            return None

        queryset.update(
            board_points=json.dumps(game_session.game.board.points),
            status=game_session.status.value,
            winner=game_session.winner,
            is_over=game_session.is_over,
            next_turn=game_session.next_turn,
        )

        db_game_session = queryset.first()
        for player in game_session.players:
            models.GameSessionPlayer.objects.update_or_create(
                id=player.id,
                item=player.item,
                game_session_id=db_game_session,
                name=player.name,
                is_host=player.is_host,
            )

        return game_session

    def save_session(self, game_session: GameSession) -> GameSession:
        board_points = json.dumps(game_session.game.board.points or [])

        db_game_session = models.GameSession.objects.create(
            id=game_session.id,
            game_name=game_session.game.name,
            board_points=board_points,
            winner=game_session.winner,
            host=game_session.host,
            status=game_session.status.value,
            is_over=game_session.is_over,
            next_turn=game_session.next_turn,
        )

        db_players = []
        for player in game_session.players:
            db_player = models.GameSessionPlayer.objects.create(
                id=player.id,
                game_session_id=db_game_session,
                name=player.name,
                is_host=player.is_host,
                item=player.item,
            )

            db_players.append(db_player)

        return game_session

    def get_session(self, session_id) -> Optional[GameSession]:
        db_game_session = models.GameSession.objects.get(id=session_id)

        if not db_game_session:
            return None

        db_players = models.GameSessionPlayer.objects.filter(
            Q(game_session_id=session_id)
        )

        game_session = self._map_to_game_session_entity(db_game_session, db_players)
        return game_session

    def list_over_player_sessions(self, player_name: str) -> List[GameSession]:
        queryset = models.GameSession.objects.filter(
            Q(gamesessionplayer__name=player_name)
            & Q(status=GameSessionStatus.OVER.value)
        )

        game_sessions = []
        for db_game_session in queryset:
            db_players = models.GameSessionPlayer.objects.filter(
                Q(game_session_id=db_game_session)
            )

            game_session = self._map_to_game_session_entity(db_game_session, db_players)
            game_sessions.append(game_session)

        return game_sessions

    def close_session(self, game_session: GameSession) -> GameSession:
        queryset = models.GameSession.objects.filter(id=game_session.id)

        if not queryset:
            return None

        queryset.update(status=GameSessionStatus.CLOSED.value)

        return game_session

    def list_open_player_sessions(self, player_name) -> List[GameSession]:
        q_conditions = Q(host=player_name) & (
            ~Q(status=GameSessionStatus.OVER.value)
            | ~Q(status=GameSessionStatus.CLOSED.value)
        )

        queryset = models.GameSession.objects.filter(q_conditions)

        game_sessions = []
        for db_game_session in queryset:
            db_players = models.GameSessionPlayer.objects.filter(
                Q(game_session_id=db_game_session)
            )

            game_session = self._map_to_game_session_entity(db_game_session, db_players)
            game_sessions.append(game_session)

        return game_sessions

    def _map_to_game_session_entity(self, db_game_session, db_players):
        players = []
        for db_player in db_players:
            player = Player(
                id=db_player.id,
                name=db_player.name,
                is_host=db_player.is_host,
                item=db_player.item,
            )
            players.append(player)

        game_session = GameSession(
            id=db_game_session.id,
            game=Game(
                name=db_game_session.game_name,
                board=Board(
                    points=json.loads(db_game_session.board_points),
                ),
            ),
            players=players,
            winner=db_game_session.winner,
            host=db_game_session.host,
            next_turn=db_game_session.next_turn,
            status=db_game_session.status,
            is_over=db_game_session.is_over,
        )

        return game_session
