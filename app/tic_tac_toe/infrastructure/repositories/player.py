from typing import Optional

from django.contrib.auth.models import User
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.repositories import IPlayerRepository


class PlayerRepository(IPlayerRepository):
    def save(self, player: Player) -> Player:
        User.objects.create_user(
            username=player.name,
            password=player.password,
        )

        return player

    def get_by_name(self, name: str) -> Optional[Player]:
        db_player = User.objects.get(username=name)

        if not db_player:
            return None

        player = Player(
            user_id=db_player.user_id,
            name=db_player.name,
        )

        return player
