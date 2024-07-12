from django.http import JsonResponse
from django.views import View
import inject
from tic_tac_toe.aplication.services import CreatePlayerService
from tic_tac_toe.presentation.rest.serializers import PlayerSerializer


class CreatePlayerView(View):
    _create_player_srv = inject.instance(CreatePlayerService)

    def post(self, request):
        player = PlayerSerializer.to_entity(request)
        created_player = self._create_player_srv.execute(player)

        response = PlayerSerializer.to_dict(created_player)

        return JsonResponse(response, status=201)
