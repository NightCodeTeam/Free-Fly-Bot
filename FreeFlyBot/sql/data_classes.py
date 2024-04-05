from dataclasses import dataclass
from datetime import datetime
from settings import SQL_BLACK_LIST

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
    def event_id(self):
        return self.__event_id
    @event_id.setter
    def event_id(self, val):
        if val in SQL_BLACK_LIST:
            self.__event_id = val

    @property
    def server_id(self):
        return self.__server_id
    @server_id.setter
    def server_id(self, val):
        if val in SQL_BLACK_LIST:
            self.__server_id = val

    @property
    def event_name(self):
        return self.__event_name
    @event_name.setter
    def event_name(self, val):
        if val in SQL_BLACK_LIST:
            self.__event_name = val

    @property
    def type_id(self):
        return self.__type_id
    @type_id.setter
    def type_id(self, val):
        if val in SQL_BLACK_LIST:
            self.__type_id = val

    @property
    def comment(self):
        return self.__comment
    @comment.setter
    def comment(self, val):
        if val in SQL_BLACK_LIST:
            self.__comment = val

    @property
    def event_time(self):
        return self.__event_time
    @event_time.setter
    def event_time(self, val):
        if val in SQL_BLACK_LIST:
            self.__event_time = val # вот объявил в базе UNIXTIME?! вот и приводи его к читаемому виду......


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
    def type_id(self):
        return self.__type_id
    @type_id.setter
    def type_id(self, val):
        if val in SQL_BLACK_LIST:
            self.__type_id = val

    @property
    def server_id(self):
        return self.__server_id
    @server_id.setter
    def server_id(self, val):
        if val in SQL_BLACK_LIST:
            self.__server_id = val

    @property
    def channel_id(self):
        return self.__channel_id
    @channel_id.setter
    def channel_id(self, val):
        if val in SQL_BLACK_LIST:
            self.__channel_id = val

    @property
    def type_name(self):
        return self.__type_name
    @type_name.setter
    def type_name(self, val):
        if val in SQL_BLACK_LIST:
            self.__type_name = val

    @property
    def role_id(self):
        return self.__role_id
    @role_id.setter
    def role_id(self, val):
        if val in SQL_BLACK_LIST:
            self.__role_id = val

    

class DiscordServer:
    def __init__(
            self,
            server_id: int,
            server_name: str
        ) -> None:
            self.server_name = server_name
            self.server_id = server_id
    @property
    def server_name(self):
        return self.__server_name
    @server_name.setter
    def server_name(self, val):
        if val in SQL_BLACK_LIST:
            self.__server_name = val

    @property
    def server_id(self):
        return self.__server_id
    @server_id.setter
    def server_id(self, val):
        if val in SQL_BLACK_LIST:
            self.__server_id = val
#@dataclass    
#class DiscordServer:
#    server_id: int
#    server_name: str
    



#@dataclass   
#class Pilot:
#    pilot_id: int
#    name: str
#    discord_nick: str
#    
#@dataclass    
#class PilotRole:
#    pilot_id: int
#    type_id: int
#    
    

