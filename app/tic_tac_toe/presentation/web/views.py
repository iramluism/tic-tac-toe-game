from typing import Any

from django.shortcuts import render
from django.views.generic import TemplateView
import inject
from tic_tac_toe.aplication import services


class IndexView(TemplateView):
    template_name = "index.html"

    _list_open_sessions_service = inject.instance(services.ListOpenGameSessionsService)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        pass


def index(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


def game(request):
    return render(request, "game.html")


def register(request):
    return render(request, "register.html")
