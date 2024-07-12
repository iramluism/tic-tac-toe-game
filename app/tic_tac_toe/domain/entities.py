from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from tic_tac_toe.domain.object_values import Board


class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))


class Player(Entity):
    user_id: str
    name: str


class Game(Entity):
    board: Board
