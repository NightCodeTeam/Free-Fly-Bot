from dataclasses import dataclass
from datetime import datetime
from .exceptions import SQLBadDataclassException
from settings import SQL_BLACK_LIST


def sql_val_good(val) -> bool:
    for i in str(val).split(' '):
        if i in SQL_BLACK_LIST:
            return False
    return True


class Event:
    def __init__(
            self,
            event_id: int,
            server_id: int,
            event_name: str,
            type_id: int,
            comment: str,
            event_time: datetime,
            event_extra_time: datetime,
            pre_pinged: bool = False
        ) -> None:
            self.event_id = event_id
            self.server_id = server_id
            self.event_name = event_name
            self.type_id = type_id
            self.comment = comment
            self.event_time = event_time
            self.event_extra_time = event_extra_time
            self.pre_pinged = pre_pinged

    def __str__(self) -> str:
        return f'ID: {self.event_id}\nServer ID: {self.server_id}\nName: {self.event_name}\nTYPE ID: {self.type_id}\nCOMMENT: {self.comment}\nDate: {self.event_time}'

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
            if type(val) is datetime:
                self.__event_time = val
            if type(val) is str:
                self.__event_time = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
        else:
            raise SQLBadDataclassException(val)

    @property
    def event_extra_time(self) -> datetime:
        return self.__event_extra_time

    @event_extra_time.setter
    def event_extra_time(self, val: datetime):
        if sql_val_good(val):
            if type(val) is datetime:
                self.__event_extra_time = val
            if type(val) is str:
                self.__event_extra_time = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
        else:
            raise SQLBadDataclassException(val)


class EventType:
    def __init__(
            self,
            type_id: int,
            server_id: int,
            type_name: str,
            channel_id: int,
            role_id: str,
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
            server_name: str,
            server_sub : bool = False
        ) -> None:
            self.server_name = server_name
            self.server_id = server_id
            self.server_sub = server_sub

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
        
    @property
    def server_sub(self) -> bool:
        return self.__server_sub

    @server_sub.setter
    def server_sub(self, val: int):
        if type(val) is bool:
            self.__server_sub = val
        elif type(val) is int:
            self.__server_sub = True if val == 1 else False
        else:
            raise SQLBadDataclassException(val)
        

class OnJoin:
    def __init__(
        self,
        onjoin_id: int,
        server_id: int,
        message: int,
        channel_listen_id: int,
        channel_admin_id: int
    ) -> None:
        self.onjoin_id = onjoin_id
        self.server_id = server_id
        self.message = message
        self.channel_listen_id = channel_listen_id
        self.channel_admin_id = channel_admin_id

    @property
    def  onjoin_id(self) -> int:
        return self.__onjoin_id
    
    
    @onjoin_id.setter
    def onjoin_id(self, val: int):
        if sql_val_good(val):
            self.__onjoin_id = val
        else:
            raise SQLBadDataclassException(val)
        

    @property
    def  server_id(self) -> int:
        return self.__server_id
    
    
    @server_id.setter
    def server_id(self, val: int):
        if sql_val_good(val):
            self.__server_id = val
        else:
            raise SQLBadDataclassException(val)
        

    @property
    def message(self) -> int:
        return self.__message
    

    @message.setter
    def message(self, val: int):
        if sql_val_good(val):
            self.__message = val
        else:
            raise SQLBadDataclassException(val)
        

    @property
    def  channel_listen_id(self) -> int:
        return self.__channel_listen_id
    

    @channel_listen_id.setter
    def channel_listen_id(self, val: int):
        if sql_val_good(val):
            self.__channel_listen_id = val
        else:
            raise SQLBadDataclassException(val)
    

    @property
    def channel_admin_id(self) -> int:
        return self.__channel_admin_id
    

    @channel_admin_id.setter
    def channel_admin_id(self, val: int):
        if sql_val_good(val):
            self.__channel_admin_id = val
        else:
            raise SQLBadDataclassException(val)
    









class OnJoinAction:
    def __init__(
        self,
        action_id: int,
        onjoin_id: int,
        button_name: str,
        button_color: str,
        role_id: int
    ) -> None:
        self.action_id = action_id 
        self.onjoin_id = onjoin_id 
        self.button_name = button_name
        self.button_color = button_color
        self.role_id = role_id

    @property
    def action_id(self) -> int:
        return self.__action_id
    
    @action_id.setter
    def action_id(self, val: int):
        if sql_val_good(val):
            self.__action_id = val
        else:
            raise SQLBadDataclassException(val)
    

    @property
    def onjoin_id(self) -> int:
        return self.__onjoin_id
    

    @onjoin_id.setter
    def onjoin_id(self, val: int):
        if sql_val_good(val):
            self.__onjoin_id = val
        else:
            raise SQLBadDataclassException(val)
    

    @property
    def button_name(self) -> str:
        return self.__button_name
    

    @button_name.setter
    def button_name(self, val: int):
        if sql_val_good(val):
            self.__button_name = val
        else:
            raise SQLBadDataclassException(val)
    

    @property
    def button_color(self) -> str: 
        return self.__button_color  
    

    @button_color.setter
    def button_color(self, val: int):
        if sql_val_good(val):
            self.__button_color = val
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
    
    


  