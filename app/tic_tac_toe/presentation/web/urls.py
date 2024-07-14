from django.urls import path
from tic_tac_toe.presentation.web import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("/login", views.login, name="login"),
    path("/game", views.GameView.as_view(), name="game"),
    path("/register", views.register, name="register"),
    path(
        "/game-session/<str:session_id>",
        views.GameSessionView.as_view(),
        name="game-session",
    ),
    path(
        "/start-game-session",
        views.StartGameSessionView.as_view(),
        name="start-game-session",
    ),
]
