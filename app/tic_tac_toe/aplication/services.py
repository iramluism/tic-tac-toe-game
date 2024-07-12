import abc

import inject
from tic_tac_toe.domain import exceptions
from tic_tac_toe.domain.entities import Player
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

    def execute(self, user_id, name: str) -> Player:
        player = self._player_repository.get_by_name(name)

        if player:
            raise exceptions.PlayerAlreadyExistsException()

        player = self._player_repository.save(user_id, name)

        return player
