from collections import namedtuple
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
