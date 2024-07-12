import abc


class Service(abc.ABC):
    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass


class CreateGameService(Service):
    def execute(self, *args, **kwargs):
        pass


class CreatePlayerService(Service):
    def execute(self, name: str):
        pass
