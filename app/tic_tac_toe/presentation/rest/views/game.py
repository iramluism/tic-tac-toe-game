import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.http import JsonResponse
from django.views import View
import inject
from tic_tac_toe.aplication import services
from tic_tac_toe.domain.exceptions import DomainException
from tic_tac_toe.presentation.rest.serializers import GameSessionTurnSerializer


class ConnectGameView(WebsocketConsumer):
    _game_session_turn_serializer = inject.instance(GameSessionTurnSerializer)
    _validate_user_session_srv = inject.instance(services.ValidateUserSessionService)
    _play_game_srv = inject.instance(services.PlayGameService)

    def _validate_player(self, request):
        headers = request.get("headers", [])

        user_session = None
        for header, value in headers:
            if header.decode("utf-8") == "authorization":
                user_session = value.decode("utf-8")
                break

        player = self._validate_user_session_srv.execute(user_session)
        return player

    def connect(self):
        self._validate_player(self.scope)

        game_session_id = self.scope["url_route"]["kwargs"]["game_session_id"]
        self.game_session_name = f"game_session_{game_session_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.game_session_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_session_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        try:
            player = self._validate_player(self.scope)

            turn = self._game_session_turn_serializer.to_entity(
                self.scope,
                player,
                json.loads(text_data),
            )

            next_turn = self._play_game_srv.execute(turn)

            message = self._game_session_turn_serializer.to_dict(next_turn)
        except DomainException as e:
            message = {"error": {"message": e.message, "code": e.code}}

        payload = {
            "type": "chat.message",
            "message": message,
        }

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(self.game_session_name, payload)

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))


class StartGameView(View):
    _validate_user_session_srv = inject.instance(services.ValidateUserSessionService)
    _start_game_srv = inject.instance(services.StartTicTacToeGameService)

    def post(self, request):
        user_session = request.headers.get("Authorization")
        player = self._validate_user_session_srv.execute(user_session)

        game_session = self._start_game_srv.execute(player_name=player.name)

        return JsonResponse(data={"game_session_id": game_session.id}, status=202)
