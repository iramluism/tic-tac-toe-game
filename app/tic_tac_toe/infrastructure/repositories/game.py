import json
from typing import Optional

from django.db.models import Q
from tic_tac_toe.domain.entities import Board
from tic_tac_toe.domain.entities import Game
from tic_tac_toe.domain.entities import GameSession
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.repositories import IGameRepository
from tic_tac_toe.domain.repositories import models


class GameRepository(IGameRepository):
    def save(self, game):
        pass

    def get(self, game_id):
        pass

    def update_session(self, game_session: GameSession) -> GameSession:
        queryset = models.GameSession.objects.filter(id=game_session.id)

        if not queryset:
            return None

        queryset.update(
            board_points=json.dumps(game_session.game.board.points),
            status=game_session.status.value,
            winner=game_session.winner,
            is_over=game_session.is_over,
        )

        return game_session

    def save_session(self, game_session: GameSession) -> GameSession:
        board_points = json.dumps(game_session.game.board.points or [])

        db_game_session = models.GameSession.objects.create(
            id=game_session.id,
            game_name=game_session.game.name,
            board_points=board_points,
            winner=game_session.winner,
            status=game_session.status.value,
            is_over=game_session.is_over,
        )

        db_players = []
        for player in game_session.players:
            db_player = models.GameSessionPlayer.objects.create(
                game_session_id=db_game_session,
                name=player.name,
                is_host=player.is_host,
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

        players = []
        for db_player in db_players:
            player = Player(name=db_player.name, is_host=db_player.is_host)
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
            status=db_game_session.status,
            is_over=db_game_session.is_over,
        )

        return game_session
