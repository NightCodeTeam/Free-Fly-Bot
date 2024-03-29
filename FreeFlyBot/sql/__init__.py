from .data_classes import (
    EventType,
    Event,
    DiscordServer,
    Pilot,
    PilotRole
)
from .create_sql import create_bd
from .server_query import (db_add_server,
                           db_check_server_for_exist,# принимает server_id возвращает True если запись есть в БД
                           db_delete_server, 
                           db_server_list) # возвращает список объектов класса DiscordServer  ну или пустой список(
from .event_query import db_add_event, db_delete_event, db_get_events
from .type_query import (db_add_type,
                         db_delete_type,
                         db_get_types,
                         db_check_type_for_exist # принимает type_id возвращает True если запись есть в БД
                         )