from django.db import models


class Player(models.Model):
    user_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
