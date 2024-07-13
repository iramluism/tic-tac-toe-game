
from django.urls import path

from tic_tac_toe_web import views


urlpatterns = [
    path("", views.index, name="index"),
]