from typing import Optional

from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.repositories import IPlayerRepository
from tic_tac_toe.infrastructure.repositories.models import Player as DBPlayer


class PlayerRepository(IPlayerRepository):
    def save(self, player: Player) -> Player:
        DBPlayer.objects.create(
            user_id=player.user_id,
            name=player.name,
        )

        return player

    def get_by_name(self, name: str) -> Optional[Player]:
        db_player = DBPlayer.objects.get(name=name)

        if not db_player:
            return None

        player = Player(
            user_id=db_player.user_id,
            name=db_player.name,
        )

        return player
