from django.http import JsonResponse
from django.views import View
import inject
from tic_tac_toe.aplication.services import CreatePlayerService


class CreatePlayerView(View):
    _create_player_srv = inject.instance(CreatePlayerService)

    def post(self, request):
        return JsonResponse(data={"done": "hola"})
