from django.urls import path
from tic_tac_toe.presentation.rest.views.player import CreatePlayerView

urlpatterns = [
    path("/player", CreatePlayerView.as_view()),
]
