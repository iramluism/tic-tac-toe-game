# Generated by Django 5.0.7 on 2024-07-12 22:36

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("tic_tac_toe", "0002_gamesession_gamesessionplayer"),
    ]

    operations = [
        migrations.AddField(
            model_name="gamesession",
            name="next_turn",
            field=models.IntegerField(default=0),
        ),
    ]
