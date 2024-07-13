from dataclasses import dataclass
from enum import Enum


class ErrorCode(Enum):
    PLAYER_ALREADY_EXISTS = 100409
    PLAYER_UNAUTHORIZED = 100401
    INVALID_USER_SESSION = 100403
    INVALID_GAME_SESSION = 101403
    INVALID_ACTION = 100400
    ACTION_NOT_ALLOWED = 100403
    PLAYER_ALREADY_CONNECTED = 100409
    POSITION_OUT_OF_BOARD = 100400


@dataclass
class DomainException(Exception):
    error_code: ErrorCode

    @property
    def message(self):
        return self.error_code.name

    @property
    def code(self):
        return self.error_code.value


@dataclass
class PlayerAlreadyExistsException(DomainException):
    error_code: ErrorCode = ErrorCode.PLAYER_ALREADY_EXISTS


@dataclass
class PlayerUnAuthorizedException(DomainException):
    error_code: ErrorCode = ErrorCode.PLAYER_UNAUTHORIZED


@dataclass
class InvalidUserSessionException(DomainException):
    error_code: ErrorCode = ErrorCode.INVALID_USER_SESSION


@dataclass
class InvalidGameSessionException(DomainException):
    error_code: ErrorCode = ErrorCode.INVALID_GAME_SESSION


@dataclass
class InvalidActionException(DomainException):
    error_code: ErrorCode = ErrorCode.INVALID_ACTION


@dataclass
class ActionNotAllowedException(DomainException):
    error_code: ErrorCode = ErrorCode.ACTION_NOT_ALLOWED


@dataclass
class PlayerAlreadyConnectedException(DomainException):
    error_code: ErrorCode = ErrorCode.PLAYER_ALREADY_CONNECTED


@dataclass
class PositionOutOfBoardException(DomainException):
    error_code: ErrorCode = ErrorCode.POSITION_OUT_OF_BOARD
