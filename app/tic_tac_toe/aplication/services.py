import abc

import inject
from tic_tac_toe.domain import exceptions
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.object_values import UserSession
from tic_tac_toe.domain.repositories import IPlayerRepository


class Service(abc.ABC):
    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass


class CreateGameService(Service):
    def execute(self, *args, **kwargs):
        pass


class CreatePlayerService(Service):
    _player_repository = inject.instance(IPlayerRepository)

    def execute(self, player: Player) -> Player:
        current_player = self._player_repository.get_by_name(name=player.name)

        if current_player:
            raise exceptions.PlayerAlreadyExistsException()

        player = self._player_repository.save(player)

        return player


class AuthenticatePlayer(Service):
    _player_repository = inject.instance(IPlayerRepository)

    def execute(self, player: Player) -> UserSession:
        authenticated_player = self._player_repository.auth(player)

        if not authenticated_player:
            raise exceptions.PlayerUnAuthorizedException()

        user_session = self._player_repository.get_user_session(player)

        return user_session
