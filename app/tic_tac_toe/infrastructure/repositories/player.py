from datetime import datetime
from datetime import timedelta
from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import jwt
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.object_values import UserSession
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

    def auth(self, player):
        user = authenticate(
            username=player.name,
            password=player.password.get_secret_value(),
        )

        return bool(user)

    def get_user_session(self, player, timeout: int = None) -> UserSession:
        timeout = timeout or settings.USER_SESSION_TIMEOUT

        payload = {
            "name": player.name,
            "exp": datetime.now() + timedelta(seconds=timeout),
        }

        session = jwt.encode(payload, key=settings.SECRET_KEY, algorithm="HS256")

        return UserSession(session)

    def validate_user_session(self, user_session: UserSession) -> Optional[Player]:
        try:
            payload = jwt.decode(
                user_session, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return None

        player = Player(name=payload["name"])

        return player
