import json
from typing import Optional

from django.http.request import HttpRequest
from tic_tac_toe.domain.entities import GameSessionTurn
from tic_tac_toe.domain.entities import Player


class PlayerSerializer:
    @classmethod
    def to_entity(self, request: HttpRequest):
        body = json.loads(request.body)
        return Player(**body)

    @classmethod
    def to_dict(self, entity: Player):
        return entity.model_dump(exclude={"password", "id"})


class GameSessionTurnSerializer:
    def to_entity(
        self, scope, player: Player, text: Optional[dict] = None
    ) -> GameSessionTurn:
        text = text or {}
        game_session_id = scope["url_route"]["kwargs"]["game_session_id"]

        turn = GameSessionTurn(
            game_session_id=game_session_id,
            player=player,
            action=text.get("action"),
            position=text.get("position"),
            item=text.get("item"),
            player_name=text.get("player_name"),
        )

        return turn

    def to_dict(self, turn: GameSessionTurn):
        data = {
            "game_session_status": turn.game_session.status.value,
            "change_status_reason": turn.change_status_reason,
            "board": turn.game_session.game.board.points,
            "player": turn.player.name,
            "next_turn": turn.game_session.next_turn_player.name,
            "is_over": turn.game_session.is_over,
        }

        return data
