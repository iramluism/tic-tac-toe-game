from django.db import models


class Player(models.Model):
    user_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)


class GameSession(models.Model):
    id = models.CharField(primary_key=True)
    board_points = models.CharField()
    winner = models.CharField(null=True, default=None)
    is_over = models.BooleanField(default=False)


class GameSessionPlayer(models.Model):
    game_session_id = models.ForeignKey("GameSession", on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
