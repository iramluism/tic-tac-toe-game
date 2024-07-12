from django.urls import path
from tic_tac_toe.presentation.rest.views import game as game_views
from tic_tac_toe.presentation.rest.views import player as player_views

urlpatterns = [
    path("/player", player_views.CreatePlayerView.as_view()),
    path("/player/auth", player_views.AuthPlayerView.as_view()),
    path("/game/start", game_views.StartGameView.as_view()),
]


websocket_urlpatterns = [
    path(r"ws/game/(?P<game_session>\w+)/$", game_views.ConnectGameView.as_asgi())
]
