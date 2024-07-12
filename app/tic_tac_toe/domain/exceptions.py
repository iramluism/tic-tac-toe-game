from dataclasses import dataclass
from enum import Enum


class ErrorCode(Enum):
    PLAYER_ALREADY_EXISTS = 100409


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
