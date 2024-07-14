from django.urls import path
from tic_tac_toe.presentation.web import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/login", views.login, name="login"),
    path("/game", views.game, name="game"),
    path("/register", views.register, name="register"),
]
