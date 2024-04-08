from typing import Final, Literal


# ! Главное
ENV_FILE: Final = ".env"
POSSIBLE_DATE_FORMATS: Final = ('\\', '/', '.', ',', ':', '-', '_')
POSSIBLE_TIME_FORMATS: Final = ('\\', '/', '.', ',', ':', '-', '_', '*')
POSSIBLE_HOUR_FORMATS: Final = ('h', 'ч')
POSSIBLE_MINUT_FORMATS: Final = ('m', 'м')

# ! Дискорд модальные окна
# ? AddEvent
DISCORD_MSH_TIMEOUT: Final = 180
ADD_EVENT_MODAL_NAME: Final = 'Создание события!'
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

#? OnJoin
ON_JOIN_MODAL_NAME: Final = 'Заполните форму:'
ON_JOIN_NAME: Final = 'Как к вам обращаться? (можно ник в игре)'
ON_JOIN_COMMENT: Final = 'Расскажите о себе:'
ON_JOIN_ALL_GOOD: Final = 'Заполненая форма отправлена администрации! Ожидайте получения роли'
ACTIONS_COLORS: Final = ('blue', 'green', 'red')

# ! Команды бота
class BotCommands:
    BOT_HELP_PREFIX = "help"
    BOT_EVENTS_PREFIX = "events"
    BOT_ADD_EVENT_PREFIX = "addevent"
    BOT_DELETE_EVENT_PREFIX = "delevent"
    BOT_TYPES_PREFIX = "types"
    BOT_ADD_TYPE_PREFIX = "addtype"
    BOT_DELETE_TYPE_PREFIX = "deltype"
    ON_JOIN = "onjoin"
    ADD_ON_JOIN = 'addjoin'
    DEL_ON_JOIN = 'deljoin'
    ON_JOIN_ACTIONS = "actions"
    ADD_ON_JOIN_ACTIONS = 'addaction'
    DEL_ON_JOIN_ACTIONS = 'delaction'


BOT_PREFIX: Final = "!"

# ! SQL
SQL_BLACK_LIST: Final = ["'","SELECT","--",'"',"DELETE",";" ]
EVENTS_TABLE_NAME: Final = "events"
TYPES_TABLE_NAME: Final = "types"
DS_SERVERS_TABLE_NAME: Final = "servers"
ON_JOIN_TABLE_NAME: Final = "onjoin"
ON_JOIN_ACTIONS_TABLE_NAME: Final = "onjoin_actions"

SQL_BD_NAME: Final = "data.db"

EVENTS_MIN_INDEX: Final = 0
EVENTS_MAX_INDEX: Final = 100

TYPES_MIN_INDEX: Final = 0
TYPES_MAX_INDEX: Final = 20

ON_JOIN_MIN_INDEX: Final = 0
ON_JOIN_MAX_INDEX: Final = 10

ON_JOIN_ACTIONS_MIN_INDEX: Final = 0
ON_JOIN_ACTIONS_MAX_INDEX: Final = 20

EVENT_NAME_MAX_CHAR: Final = 30
EVENT_DATE_MAX_CHAR: Final = 10
EVENT_TIME_MAX_CHAR: Final = 11
EVENT_COMMENT_MAX_CHAR: Final = 300
TYPE_NAME_MAX_CHAR: Final = 15
SERVER_NAME_MAX_CHAR: Final = 50
ON_JOIN_MESSAGE_MAX_CHAR: Final = 300
ON_JOIN_ACTION_BUTTON_MAX_CHAR: Final = 30
ON_JOIN_ACTION_BUTTON_COLOR_MAX_CHAR: Final = 5


CREATE_TABLE_EVENTS: Final = f"""CREATE TABLE IF NOT EXISTS {EVENTS_TABLE_NAME} (
    event_id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    event_name VARCHAR({EVENT_NAME_MAX_CHAR}),
    type_id INTEGER NOT NULL,
    comment VARCHAR({EVENT_COMMENT_MAX_CHAR}),
    event_time TIMESTAMP NOT NULL,
    event_extra_time TIMESTAMP NOT NULL,
    FOREIGN KEY(server_id) REFERENCES {DS_SERVERS_TABLE_NAME}(server_id) ON DELETE CASCADE,
    FOREIGN KEY(type_id) REFERENCES {TYPES_TABLE_NAME}(type_id) ON DELETE CASCADE);"""

CREATE_TABLE_TYPES: Final = f"""CREATE TABLE IF NOT EXISTS {TYPES_TABLE_NAME} (
    type_id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    type_name VARCHAR({TYPE_NAME_MAX_CHAR}) NOT NULL,
    channel_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY(server_id) REFERENCES {DS_SERVERS_TABLE_NAME}(server_id) ON DELETE CASCADE);"""

CREATE_TABLE_SERVERS: Final = f"""CREATE TABLE IF NOT EXISTS {DS_SERVERS_TABLE_NAME} (
    server_id INTEGER PRIMARY KEY,
    server_name VARCHAR({SERVER_NAME_MAX_CHAR}) UNIQUE,
    server_sub BOOLEAN NOT NULL);"""

CREATE_TABLE_ON_JOIN: Final = f"""CREATE TABLE IF NOT EXISTS {ON_JOIN_TABLE_NAME} (
    onjoin_id INTEGER PRIMARY KEY ON DELETE CASCADE,
    server_id INTEGER UNIQUE,
    message VARCHAR({ON_JOIN_MESSAGE_MAX_CHAR}) NOT NULL,
    channel_listen_id INTEGER NOT NULL,
    channel_admin_id INTEGER NOT NULL,
    FOREIGN KEY(server_id) REFERENCES {DS_SERVERS_TABLE_NAME}(server_id) ON DELETE CASCADE);"""

CREATE_TABLE_ON_JOIN_ACTIONS: Final = f"""CREATE TABLE IF NOT EXISTS {ON_JOIN_ACTIONS_TABLE_NAME} (
    action_id INTEGER PRIMARY KEY,
    onjoin_id INTEGER NOT NULL,
    button_name VARCHAR({ON_JOIN_ACTION_BUTTON_MAX_CHAR}) NOT NULL,
    button_color VARCHAR({ON_JOIN_ACTION_BUTTON_COLOR_MAX_CHAR}) NOT NULL,
    FOREIGN KEY(onjoin_id) REFERENCES {ON_JOIN_TABLE_NAME}(onjoin_id) ON DELETE CASCADE);"""