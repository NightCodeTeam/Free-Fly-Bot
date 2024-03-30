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
                           db_server_list) # возвращает список объектов класса DiscordServer  ну или пустой список(
from .event_query import db_add_event, db_delete_event, db_get_events
from .type_query import (db_add_type, # принимает объект класса EventType
                         db_delete_type,# принимает type_id (int)
                         db_get_types,
                         db_check_type_for_exist # принимает type_id возвращает True если запись есть в БД
                         )