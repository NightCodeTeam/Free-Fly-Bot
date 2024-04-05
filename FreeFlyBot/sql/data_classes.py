from dataclasses import dataclass
from datetime import datetime
from .exceptions import SQLBadDataclassException
from settings import SQL_BLACK_LIST


def sql_val_good(val) -> bool:
    return False if str(val) in SQL_BLACK_LIST else True


class Event:
    def __init__(
            self,
            event_id: int,
            server_id: int,
            event_name: str,
            type_id: int,
            comment: str,
            event_time: datetime
        ) -> None:
            self.event_id = event_id
            self.server_id = server_id
            self.event_name = event_name
            self.type_id = type_id
            self.comment = comment
            self.event_time = event_time

    @property
    def event_id(self) -> int:
        return self.__event_id

    @event_id.setter
    def event_id(self, val: int):
        if sql_val_good(val):
            self.__event_id = val
        else:
            raise SQLBadDataclassException(val)

    @property
    def server_id(self) -> int:
        return self.__server_id

    @server_id.setter
    def server_id(self, val: int):
        if sql_val_good(val):
            self.__server_id = val
        else:
            raise SQLBadDataclassException(val)

    @property
    def event_name(self) -> str:
        return self.__event_name

    @event_name.setter
    def event_name(self, val: str):
        if sql_val_good(val):
            self.__event_name = val
        else:
            raise SQLBadDataclassException(val)

    @property
    def type_id(self) -> int:
        return self.__type_id

    @type_id.setter
    def type_id(self, val: int):
        if sql_val_good(val):
            self.__type_id = val
        else:
            raise SQLBadDataclassException(val)

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, val: str):
        if sql_val_good(val):
            self.__comment = val
        else:
            raise SQLBadDataclassException(val)

    @property
    def event_time(self) -> datetime:
        return self.__event_time

    @event_time.setter
    def event_time(self, val: datetime):
        if sql_val_good(val):
            self.__event_time = val
        else:
            raise SQLBadDataclassException(val)


class EventType:
    def __init__(
            self,
            type_id: int,
            server_id: int,
            type_name: str,
            channel_id: int,
            role_id: int,
        ) -> None:
            self.type_id = type_id
            self.server_id = server_id
            self.type_name = type_name
            self.channel_id = channel_id
            self.role_id = role_id

    @property
    def type_id(self) -> int:
        return self.__type_id

    @type_id.setter
    def type_id(self, val: int):
        if sql_val_good(val):
            self.__type_id = val
        else:
            raise SQLBadDataclassException(val)

    @property
    def server_id(self) -> int:
        return self.__server_id

    @server_id.setter
    def server_id(self, val: int):
        if sql_val_good(val):
            self.__server_id = val
        else:
            raise SQLBadDataclassException(val)

    @property
    def channel_id(self) -> int:
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, val: int):
        if sql_val_good(val):
            self.__channel_id = val
        else:
            raise SQLBadDataclassException(val)

    @property
    def type_name(self) -> str:
        return self.__type_name

    @type_name.setter
    def type_name(self, val: str):
        if sql_val_good(val):
            self.__type_name = val
        else:
            raise SQLBadDataclassException(val)

    @property
    def role_id(self) -> int:
        return self.__role_id

    @role_id.setter
    def role_id(self, val: int):
        if sql_val_good(val):
            self.__role_id = val
        else:
            raise SQLBadDataclassException(val)


class DiscordServer:
    def __init__(
            self,
            server_id: int,
            server_name: str
        ) -> None:
            self.server_name = server_name
            self.server_id = server_id

    @property
    def server_name(self) -> str:
        return self.__server_name

    @server_name.setter
    def server_name(self, val: str):
        if sql_val_good(val):
            self.__server_name = val
        else:
            raise SQLBadDataclassException(val)

    @property
    def server_id(self) -> int:
        return self.__server_id

    @server_id.setter
    def server_id(self, val: int):
        if sql_val_good(val):
            self.__server_id = val
        else:
            raise SQLBadDataclassException(val)
