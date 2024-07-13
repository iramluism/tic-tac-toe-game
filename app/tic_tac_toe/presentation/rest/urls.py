from django.urls import path
from django.urls import re_path
from tic_tac_toe.presentation.rest.views import game as game_views
from tic_tac_toe.presentation.rest.views import player as player_views

urlpatterns = [
    path("/player", player_views.CreatePlayerView.as_view()),
    path("/player/auth", player_views.AuthPlayerView.as_view()),
    path("/games/start", game_views.StartGameView.as_view()),
    path("/games", game_views.ListGameSessionsView.as_view()),
]

websocket_urlpatterns = [
    re_path(
        r"ws/game/(?P<game_session_id>[\w-]+)/$", game_views.ConnectGameView.as_asgi()
    )
]
