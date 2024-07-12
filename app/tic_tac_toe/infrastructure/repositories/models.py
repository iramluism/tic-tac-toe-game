from django.db import models


class Player(models.Model):
    user_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)


class GameSession(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    board_points = models.CharField(max_length=200)
    winner = models.CharField(null=True, default=None, max_length=20)
    next_turn = models.IntegerField(default=0)
    is_over = models.BooleanField(default=False)


class GameSessionPlayer(models.Model):
    game_session_id = models.ForeignKey("GameSession", on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
