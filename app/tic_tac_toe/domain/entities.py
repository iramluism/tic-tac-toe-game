from typing import List
from typing import Optional
from typing import Tuple
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator
from pydantic import SecretStr
from tic_tac_toe.domain import exceptions
from tic_tac_toe.domain.object_values import GameSessionStatus
from tic_tac_toe.domain.object_values import Item
from tic_tac_toe.domain.object_values import PlayerAction
from tic_tac_toe.domain.object_values import Position


class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))


class Player(Entity):
    name: str
    password: Optional[SecretStr] = None
    is_host: bool = False
    item: Optional[Item] = None


class Board(BaseModel):
    points: Optional[List[List]] = None
    size: Tuple = None

    @model_validator(mode="after")
    def validate_size(self):
        size = self.size
        points = self.points

        if not size and points:
            h = len(points)
            w = len(points[0])
            self.size = (h, w)

        elif size and not points:
            h, w = size
            self.points = [[None] * w] * h

        elif not size and not points:
            raise ValueError("Size or points are required")

        return self

    def set_item(self, position: Position, item: Item):
        self.points[position.y][position.x] = item

    def get_item(self, position: Position):
        return self.points[position.y][position.y]

    def is_full(self):
        return all(all(x_axis) for x_axis in self.points)

    def get_vector(self):
        h, w = self.size

        for y in range(h):
            yield self.points[y]

        for x in range(w):
            yield [self.points[y][x] for y in range(h)]

        yield [self.points[i][i] for i in range(h)]
        yield [self.points[i][h - i - 1] for i in range(h)]


class Game(Entity):
    name: str
    board: Board


class GameSession(Entity):
    game: Game
    status: GameSessionStatus = GameSessionStatus.WAITING_FOR_PLAYER
    players: List[Player]
    next_turn: int = 0
    winner: Optional[Player] = None
    is_over: bool = False

    @property
    def host(self):
        return self.players[0]

    def set_next_turn(self):
        self.next_turn = (self.next_turn + 1) % len(self.players)

    @property
    def next_turn_player(self):
        return self.players[self.next_turn]

    def add_player(self, player: Player):
        for already_added_player in self.players:
            if already_added_player.name == player.name:
                raise exceptions.PlayerAlreadyConnectedException()

        self.players.append(player)


class TicTacToeGame(Game):
    name: str = "TicTacToe"
    board: Board = Field(default_factory=lambda: Board(size=(3, 3)))


class GameSessionTurn(Entity):
    game_session_id: str
    game_session: Optional[GameSession] = None
    player: Player
    player_name: Optional[str] = None
    action: PlayerAction
    item: Optional[Item] = None
    position: Optional[Position] = None
    change_to_status: Optional[GameSessionStatus] = None
    change_status_reason: Optional[str] = None
