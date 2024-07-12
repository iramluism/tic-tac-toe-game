from typing import List

from tic_tac_toe.domain.entities import Entity
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.object_values import Game


class GameSession(Entity):
    game: Game
    players: List[Player]
    current_player: Player
    winner: Player
    is_over: bool
