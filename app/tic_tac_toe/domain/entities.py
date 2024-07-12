from typing import List
from typing import Optional
from typing import Tuple
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic import SecretStr
from pydantic import validator
from tic_tac_toe.domain.object_values import Item
from tic_tac_toe.domain.object_values import Position


class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))


class Player(Entity):
    name: str
    password: Optional[SecretStr] = None
    is_host: bool = False


class Board(BaseModel):
    points: Optional[List[List]] = None
    size: Tuple = None

    @validator("points", pre=False)
    def validate_points(cls, points, values):
        if not points:
            h, w = values.size
            values.points = [[None] * w] * h

        return values

    @validator("size", pre=False)
    def validate_size(cls, size, values):
        if not size and values.points:
            h = len(values.points)
            w = len(values.points[0])
            values.size = (h, w)

    def set_item(self, position: Position, item: Item):
        self.points[position.y][position.x] = item

    def get_item(self, position: Position):
        return self.points[position.y][position.y]

    def is_full(self):
        return all(all(x_axis) for x_axis in self.points)


class Game(Entity):
    name: str
    board: Board


class GameSession(Entity):
    game: Game
    players: List[Player]
    next_turn: int = 0
    winner: Optional[Player] = None
    is_over: bool = False


class TicTacToeGame(Game):
    name: str = "TicTacToe"
    board: Board = Field(default_factory=lambda: Board(size=(3, 3)))
