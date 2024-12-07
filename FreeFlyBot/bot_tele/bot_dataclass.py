from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str


@dataclass(frozen=True, slots=True)
class Chat:
    id: int
    first_name: str
    last_name: str
    username: str
    type: Literal['private', '']


@dataclass(frozen=True, slots=True)
class Message:
    message_id: int
    user: User
    chat: Chat
    date: int
    text: str | None


@dataclass(frozen=True, slots=True)
class CallbackQuery:
    id: int
    user: User
    message: Message
    chat_instance: int
    data: str


@dataclass(frozen=True, slots=True)
class Update:
    update_id: int
    message: Message


@dataclass(frozen=True, slots=True)
class UpdateCallback:
    update_id: int
    callback_query: CallbackQuery
