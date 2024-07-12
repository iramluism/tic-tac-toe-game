from typing import Optional

from django.contrib.auth.models import User
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.repositories import IPlayerRepository


class PlayerRepository(IPlayerRepository):
    def save(self, player: Player) -> Player:
        User.objects.create_user(
            username=player.name,
            password=player.password.get_secret_value(),
        )

        return player

    def get_by_name(self, name: str) -> Optional[Player]:
        try:
            db_player = User.objects.get(username=name)
        except User.DoesNotExist:
            return None

        player = Player(
            name=db_player.username,
        )

        return player
