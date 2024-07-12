from pydantic import BaseModel, Field
from uuid import uuid4
from tic_tac_toe.domain.object_values import Board


class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))


class Player(Entity):
    name: str


class Game(Entity):
    board: Board
