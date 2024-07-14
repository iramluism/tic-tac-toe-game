from typing import Any

from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView
import inject
from tic_tac_toe.aplication import services
from tic_tac_toe.domain.exceptions import InvalidUserSessionException
from tic_tac_toe.presentation.web import utils


class IndexView(TemplateView):
    template_name = "index.html"

    _list_open_sessions_srv = inject.instance(services.ListOpenGameSessionsService)
    _validate_user_session_srv = inject.instance(services.ValidateUserSessionService)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user_session = self.request.COOKIES.get("userSession")

        try:
            self._validate_user_session_srv.execute(user_session)
        except InvalidUserSessionException:
            redirect("/web/login")

        open_sessions = self._list_open_sessions_srv.execute()

        open_session_ctx = []
        for session in open_sessions:
            open_session_ctx.append(
                {
                    "id": session.id,
                    "host": session.host.name,
                }
            )

        return {"open_sessions": open_session_ctx}


class GameSessionView(TemplateView):
    template_name = "game_session.html"

    _get_game_session_srv = inject.instance(services.GetGameSessionService)
    _validate_user_session_srv = inject.instance(services.ValidateUserSessionService)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user_session = self.request.COOKIES.get("userSession")
        if not utils.validate_user_session(user_session):
            return redirect("/web/login")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        session_id = self.kwargs["session_id"]
        game_session = self._get_game_session_srv.execute(session_id)

        context = {
            "session_id": game_session.id,
            "host": game_session.host.name,
        }

        return context


def index(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


def game(request):
    return render(request, "game.html")


def register(request):
    return render(request, "register.html")
