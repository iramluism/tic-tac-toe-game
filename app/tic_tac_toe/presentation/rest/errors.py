from http import HTTPStatus

from tic_tac_toe.domain.exceptions import ErrorCode

ErrorCodeMap = {
    ErrorCode.PLAYER_ALREADY_EXISTS: HTTPStatus.CONFLICT,  # 409
}


def get_status_code(error_code: ErrorCode):
    return ErrorCodeMap.get(error_code, HTTPStatus.INTERNAL_SERVER_ERROR)
