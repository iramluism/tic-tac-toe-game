from dataclasses import dataclass
from enum import Enum


class ErrorCode(Enum):
    PLAYER_ALREADY_EXISTS = 100409
    PLAYER_UNAUTHORIZED = 100401
    INVALID_USER_SESSION = 100403


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
