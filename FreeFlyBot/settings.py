from typing import Final


# ! Главное
ENV_FILE: Final = ".env"
POSSIBLE_DATE_FORMATS: Final = ('\\', '/', '.', ',', ':', '-', '_')
POSSIBLE_TIME_FORMATS: Final = ('\\', '/', '.', ',', ':', '-', '_', '*')
POSSIBLE_HOUR_FORMATS: Final = ('h', 'ч')
POSSIBLE_MINUT_FORMATS: Final = ('m', 'м')

# ! Дискорд модальные окна
DISCORD_MSH_TIMEOUT: Final = 180
ADD_EVENT_VIEW_NAME: Final = 'Название:'
ADD_EVENT_VIEW_NAME_PLACEHOLDER: Final = 'Название события'
EVENT_TYPE_SELECTOR_PLACEHOLDER: Final = 'Выберите тип события:'
ADD_EVENT_DATE_NAME: Final = 'Дата:'
ADD_EVENT_DATE_PLACEHOLDER: Final = '2024.12.31'
ADD_EVENT_TIME_NAME: Final = 'Время:'
ADD_EVENT_TIME_PLACEHOLDER: Final = '24:00'
ADD_EVENT_ONE_PING_BEFORE_NAME: Final = 'Засколько часов пингануть?'
ADD_EVENT_ONE_PING_BEFORE_PLACEHOLDER: Final = '0'
ADD_EVENT_COMMENT_NAME: Final = 'Комментарий:'
ADD_EVENT_COMMENT_PLACEHOLDER: Final = ''
CONFIRM_BUTTON: Final = 'Подтвердить'
CANCEL_BUTTON: Final = 'Отмена'

# ! Команды бота
class BotCommands:
    BOT_HELP_PREFIX = "help"
    BOT_EVENTS_PREFIX = "events"
    BOT_ADD_EVENT_PREFIX = "addevent"
    BOT_DELETE_EVENT_PREFIX = "delevent"
    BOT_TYPES_PREFIX = "types"
    BOT_ADD_TYPE_PREFIX = "addtype"
    BOT_DELETE_TYPE_PREFIX = "deltype"


BOT_PREFIX: Final = "!"

# ! SQL
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

EVENT_NAME_MAX_CHAR: Final = 30
EVENT_DATE_MAX_CHAR: Final = 10
EVENT_TIME_MAX_CHAR: Final = 11
EVENT_COMMENT_MAX_CHAR: Final = 300
TYPE_NAME_MAX_CHAR: Final = 15
SERVER_NAME_MAX_CHAR: Final = 50

CREATE_TABLE_EVENTS: Final = f"""CREATE TABLE IF NOT EXISTS {EVENTS_TABLE_NAME} (
    event_id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    event_name VARCHAR({EVENT_NAME_MAX_CHAR}),
    type_id INTEGER NOT NULL,
    comment VARCHAR({EVENT_COMMENT_MAX_CHAR}),
    event_time TIMESTAMP NOT NULL,
    FOREIGN KEY(server_id) REFERENCES servers(server_id),
    FOREIGN KEY(type_id) REFERENCES types(type_id));"""

CREATE_TABLE_TYPES: Final = f"""CREATE TABLE IF NOT EXISTS {TYPES_TABLE_NAME} (
    type_id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    type_name VARCHAR({TYPE_NAME_MAX_CHAR}) NOT NULL,
    channel_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY(server_id) REFERENCES servers(server_id));"""

CREATE_TABLE_SERVERS: Final = f"""CREATE TABLE IF NOT EXISTS {DS_SERVERS_TABLE_NAME} (
    server_id INTEGER PRIMARY KEY,
    server_name VARCHAR({SERVER_NAME_MAX_CHAR}) UNIQUE);"""
