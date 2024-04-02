from typing import Final


EVENT_TYPE_SELECTOR_PLACEHOLDER: Final = 'Выберите тип события:'


class BotCommands:
    BOT_HELP_PREFIX = "help"
    BOT_EVENTS_PREFIX = "events"
    BOT_ADD_EVENT_PREFIX = "addevent"
    BOT_DELETE_EVENT_PREFIX = "delevent"
    BOT_TYPES_PREFIX = "types"
    BOT_ADD_TYPE_PREFIX = "addtype"
    BOT_DELETE_TYPE_PREFIX = "deltype"


ENV_FILE: Final = ".env"

BOT_PREFIX: Final = "!"
EVENTS_TABLE_NAME: Final = "events"
TYPES_TABLE_NAME: Final = "types"
DS_SERVERS_TABLE_NAME: Final = "servers"
PILOTS_TABLE_NAME: Final = ""
PILOT_ROLES_TABLE_NAME: Final = ""

SQL_BD_NAME: Final = "data.db"

EVENTS_MIN_INDEX: Final = 0
EVENTS_MAX_INDEX: Final = 100

TYPES_MIN_INDEX: Final = 0
TYPES_MAX_INDEX: Final = 20

CREATE_TABLE_EVENTS: Final = f"""CREATE TABLE IF NOT EXISTS {EVENTS_TABLE_NAME} (
    event_id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    event_name VARCHAR(30),
    type_id INTEGER NOT NULL,
    comment VARCHAR(300),
    event_time TIMESTAMP NOT NULL,
    FOREIGN KEY(server_id) REFERENCES servers(server_id),
    FOREIGN KEY(type_id) REFERENCES types(type_id));"""

CREATE_TABLE_TYPES: Final = f"""CREATE TABLE IF NOT EXISTS {TYPES_TABLE_NAME} (
    type_id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    type_name VARCHAR(15) NOT NULL,
    channel_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY(server_id) REFERENCES servers(server_id));"""

CREATE_TABLE_SERVERS: Final = f"""CREATE TABLE IF NOT EXISTS {DS_SERVERS_TABLE_NAME} (
    server_id INTEGER PRIMARY KEY,
    server_name VARCHAR(50) UNIQUE);"""