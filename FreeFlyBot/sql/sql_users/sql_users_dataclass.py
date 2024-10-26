from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    id: int
    username: str


@dataclass(frozen=True, slots=True)
class UserBanned:
    id: int
    username: str
    reason: str = 'нет'
