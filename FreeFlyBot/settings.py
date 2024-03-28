from typing import Final


class BotCommands:
    BOT_HELP_PREFIX = "help"
    BOT_EVENTS_PREFIX = "events"
    BOT_ADD_EVENT_PREFIX = "addevent"
    BOT_DELETE_EVENT_PREFIX = "delevent"
    BOT_TYPES_PREFIX = "types"
    BOT_ADD_TYPE_PREFIX = "addtype"
    BOT_DELETE_TYPE_PREFIX = "removetype"


ENV_FILE: Final = ".env"

BOT_PREFIX: Final = "!"

SQL_BD_NAME: Final = "data.sqlite"

EVENTS: Final = ""
TYPES: Final = ""
DS_SERVERS: Final = ""
PILOTS: Final = ""
PILOT_ROLES: Final = ""
DB_NAME: Final = ""

CREATE_TABLE_EVENTS: Final = """CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    event_name VARCHAR(30),
    type_id INTEGER NOT NULL,
    comment VARCHAR(300),
    event_time TIMESTAMP NOT NULL,
    FOREIGN KEY(server_id) REFERENCES servers(server_id),
    FOREIGN KEY(type_id) REFERENCES types(type_id));"""

CREATE_TABLE_TYPES: Final = """CREATE TABLE IF NOT EXISTS types (
    type_id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    type_name VARCHAR(15) NOT NULL, 
    channel VARCHAR(30) NOT NULL,
    role_name VARCHAR(30) NOT NULL,
    FOREIGN KEY(server_id) REFERENCES servers(server_id));"""

CREATE_TABLE_SERVERS: Final = """CREATE TABLE IF NOT EXISTS servers (
    server_id INTEGER PRIMARY KEY,
    server_name VARCHAR(50) UNIQUE);"""