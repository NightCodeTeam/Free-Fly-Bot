from .data_classes import (
    EventType,
    Event,
    DiscordServer,
    Pilot,
    PilotRole
)
from .create_sql import create_bd
from .adt_query import (
    db_create_event_id,
    db_create_type_id,
)


from .server_query import (
    db_add_server,   # принимает объект класса DiscordServer
    db_check_server_for_exist,# принимает server_id (int)     возвращает True если запись есть в БД
    db_delete_server,  # принимает server_id (int)
    db_server_list,  # возвращает список объектов класса DiscordServer 
    db_get_server_by_id 
) 


from .event_query import (
    db_add_event, # принимает об. класса Event
    db_delete_event, # принимает event_id (int) 
    db_get_events_by_type, #### принимает СПИСОК type_id возвращает список об. кл. Event
    db_get_events_list, ### возвращает список всех ивентов (Event)
    db_check_event_for_exist, ### принимает event_id возвращает Ture если такой id есть в БД
    db_get_event_by_id #принимает event_id  возвращает ОБЪЕКТ Event 
)


from .type_query import (
    db_add_type, # принимает объект класса EventType
    db_delete_type,# принимает type_id (int)
    db_types_list, # возвоащает список объектов EventType
    db_check_type_for_exist, # принимает type_id возвращает True если запись есть в БД
    db_get_type_by_id,
    db_types_list_by_server_id, ###
    db_get_type_by_name_and_server_id ### принмает server_id (int) & type_name (str)
)