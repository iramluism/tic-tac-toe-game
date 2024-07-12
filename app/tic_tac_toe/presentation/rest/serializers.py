import json

from django.http.request import HttpRequest
from tic_tac_toe.domain.entities import Player


class PlayerSerializer:
    @classmethod
    def to_entity(self, request: HttpRequest):
        body = json.loads(request.body)
        return Player(**body)

    @classmethod
    def to_dict(self, entity: Player):
        return entity.model_dump(exclude={"password"})
