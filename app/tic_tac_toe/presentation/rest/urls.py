from django.urls import path
from tic_tac_toe.presentation.rest.views import player as player_views

urlpatterns = [
    path("/player", player_views.CreatePlayerView.as_view()),
    path("/player/auth", player_views.AuthPlayerView.as_view()),
]
