from .data_classes import (
    EventType,
    Event,
    DiscordServer,
    Pilot,
    PilotRole
)
from .create_sql import create_bd
from .server_query import (db_add_server,   # принимает объект класса DiscordServer
                           db_check_server_for_exist,# принимает server_id (int)     возвращает True если запись есть в БД
                           db_delete_server,  # принимает server_id (int)
                           db_server_list
                          ) # возвращает список объектов класса DiscordServer 
 

from .event_query import (db_add_event, # принимает об. класса Event
                          db_delete_event, # принимает event_id (int) 
                          db_get_events_by_type, ####
                          db_get_events_list ###
                         )


from .type_query import (db_add_type, # принимает объект класса EventType
                         db_delete_type,# принимает type_id (int)
                         db_types_list, # возвоащает список объектов EventType
                         db_check_type_for_exist # принимает type_id возвращает True если запись есть в БД
                        )