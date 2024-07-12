import json

from channels.generic.websocket import WebsocketConsumer
from django.http import JsonResponse
from django.views import View
import inject
from tic_tac_toe.aplication import services


class ConnectGameView(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))


class StartGameView(View):
    _validate_user_session_srv = inject.instance(services.ValidateUserSessionService)
    _start_game_srv = inject.instance(services.StartTicTacToeGameService)

    def post(self, request):
        user_session = request.headers.get("Authorization")
        player = self._validate_user_session_srv.execute(user_session)

        game_session = self._start_game_srv.execute(player_name=player.name)

        return JsonResponse(data={"game_session_id": game_session.id}, status=202)
