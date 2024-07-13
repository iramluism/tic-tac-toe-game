from collections import namedtuple
from enum import Enum
from typing import NewType

UserSession = NewType("UserSession", str)


Position = namedtuple("Position", ["x", "y"])

Item = NewType("Item", str)

NOUGHT = "O"
CROSS = "X"


EmptyBoard3x3 = [
    [None, None, None],
    [None, None, None],
    [None, None, None],
]


class PlayerAction(Enum):
    CONNECT = "connect"
    MARK = "mark"
    QUIT = "quit"
    ADMIT_PLAYER = "admit_player"
    RESUME = "resume"


class GameSessionStatus(Enum):
    WAITING_FOR_PLAYER = "WAITING_FOR_PLAYER"
    WAITING_FOR_HOST_APPROVAL = "WAITING_FOR_HOST_APPROVAL"
    RUNNING = "RUNNING"
    OVER = "OVER"
