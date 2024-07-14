import inject
from tic_tac_toe.aplication import services
from tic_tac_toe.domain.exceptions import InvalidUserSessionException


@inject.param("validate_user_session_srv", services.ValidateUserSessionService)
def validate_user_session(
    user_session: str, validate_user_session_srv, redirect_to="login"
):
    try:
        player = validate_user_session_srv.execute(user_session)
    except InvalidUserSessionException:
        return False

    return player
