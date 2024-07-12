import json
from typing import Optional

from django.db.models import Q
from tic_tac_toe.domain.entities import Board
from tic_tac_toe.domain.entities import Game
from tic_tac_toe.domain.entities import GameSession
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.repositories import IGameRepository
from tic_tac_toe.infrastructure.repositories.models import GameSession as DBGameSession
from tic_tac_toe.infrastructure.repositories.models import (
    GameSessionPlayer as DBGameSessionPlayer,
)


class GameRepository(IGameRepository):
    def save(self, game):
        pass

    def get(self, game_id):
        pass

    def save_session(self, game_session: GameSession) -> GameSession:
        db_players = []
        for player in game_session.players:
            db_player = DBGameSessionPlayer.objects.create(
                game_session_id=game_session.id, name=player.name
            )

            db_players.append(db_player)

        DBGameSession.objects.create(
            id=game_session.id,
            board_points=json.dumps(game_session.game.board.points),
            winner=game_session.winner,
            is_over=game_session.is_over,
        )

        return game_session

    def get_session(self, session_id) -> Optional[GameSession]:
        db_game_session = DBGameSession.objects.filter(Q(game_session_id=session_id))

        if not db_game_session:
            return None

        db_players = DBGameSessionPlayer.objects.filter(Q(game_session_id=session_id))

        players = []
        for db_player in db_players:
            player = Player(name=db_player.name)
            players.append(player)

        game_session = GameSession(
            game=Game(
                board=Board(
                    points=json.loads(db_game_session.points),
                ),
            ),
            players=players,
            winner=db_game_session.winner,
            is_over=db_game_session.is_over,
        )

        return game_session
