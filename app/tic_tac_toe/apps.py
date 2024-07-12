from django.apps import AppConfig


class TicTacToeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tic_tac_toe"

    def ready(self):
        from tic_tac_toe.infrastructure.setup import setup_app

        setup_app()
