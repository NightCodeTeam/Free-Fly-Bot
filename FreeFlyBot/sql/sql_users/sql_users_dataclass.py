from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    id: int
    username: str


@dataclass(frozen=True, slots=True)
class UserBanned:
    user_id: int
    reason: str = 'не указано'
