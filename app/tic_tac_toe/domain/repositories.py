from typing import Optional

from tic_tac_toe.domain.entities import Game
from tic_tac_toe.domain.entities import Player


class IGameRepository:
    def save(self, game: Game):
        raise NotImplementedError()

    def get(self, game_id: str) -> Game:
        raise NotImplementedError()


class IPlayerRepository:
    def save(self, player) -> Player:
        raise NotImplementedError()

    def get(self, player_id: str) -> Optional[Player]:
        raise NotImplementedError()
