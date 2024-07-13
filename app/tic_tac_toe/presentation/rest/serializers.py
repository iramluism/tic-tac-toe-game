import json

from django.http.request import HttpRequest
from tic_tac_toe.domain.entities import GameSessionTurn
from tic_tac_toe.domain.entities import Player
from tic_tac_toe.domain.object_values import PlayerAction


class PlayerSerializer:
    @classmethod
    def to_entity(self, request: HttpRequest):
        body = json.loads(request.body)
        return Player(**body)

    @classmethod
    def to_dict(self, entity: Player):
        return entity.model_dump(exclude={"password", "id"})


class GameSessionTurnSerializer:
    def to_entity(self, scope, player: Player, action: PlayerAction) -> GameSessionTurn:
        game_session_id = scope["url_route"]["kwargs"]["game_session_id"]

        turn = GameSessionTurn(
            game_session_id=game_session_id,
            player=player,
            action=action,
        )

        return turn

    def to_dict(self, turn: GameSessionTurn):
        data = {
            "game_session_status": turn.change_to_status.value,
            "change_status_reason": turn.change_status_reason,
        }

        return data
