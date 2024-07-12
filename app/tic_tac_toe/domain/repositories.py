from typing import Optional

from tic_tac_toe.domain.entities import Game
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.object_values import UserSession


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

    def auth(self, player: Player) -> bool:
        raise NotImplementedError()

    def get_user_session(self, player: Player, timeout: int) -> UserSession:
        raise NotImplementedError()
