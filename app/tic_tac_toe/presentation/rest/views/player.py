from django.http import JsonResponse
from django.views import View
import inject
from tic_tac_toe.application import services
from tic_tac_toe.presentation.rest.serializers import PlayerSerializer


class CreatePlayerView(View):
    _create_player_srv = inject.instance(services.CreatePlayerService)
    _authenticate_player_srv = inject.instance(services.AuthenticatePlayer)

    def post(self, request):
        player = PlayerSerializer.to_entity(request)

        created_player = self._create_player_srv.execute(player)
        user_session = self._authenticate_player_srv.execute(created_player)

        response = JsonResponse(data={"user_session": user_session}, status=201)

        return response


class AuthPlayerView(View):
    _authenticate_player_srv = inject.instance(services.AuthenticatePlayer)

    def post(self, request):
        player = PlayerSerializer.to_entity(request)
        user_session = self._authenticate_player_srv.execute(player)

        response = JsonResponse(data={"user_session": user_session}, status=201)

        return response
