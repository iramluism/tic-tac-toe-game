from typing import Optional
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic import SecretStr
from tic_tac_toe.domain.object_values import Board


class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))


class Player(Entity):
    name: str
    password: Optional[SecretStr] = None


class Game(Entity):
    board: Board
