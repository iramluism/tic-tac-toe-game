from pydantic import BaseModel
from collections import namedtuple


Position = namedtuple('Position', ['x', 'y'])


class Item(BaseModel):
    name: str 


class Board(BaseModel):

    def set_item(self, position: Position, item: Item):
        pass

    def get_item(self, position: Position):
        pass

    def is_full(self):
        pass

