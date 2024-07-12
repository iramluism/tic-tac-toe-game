from tic_tac_toe.domain.entities import Game


class IGameRepository:
    def save(self, game: Game):
        raise NotImplementedError()

    def get(self, game_id: str) -> Game:
        raise NotImplementedError()


class IPlayerRepository:
    def save(self, player):
        raise NotImplementedError()

    def get(self, player_id: str):
        raise NotImplementedError()
