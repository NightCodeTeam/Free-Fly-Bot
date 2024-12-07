from typing import Final


# ! Основа
ENV_FILE: Final = '.env'
FOLDER_FILES: Final = 'data'

# ! SQL
SQL_DATABASE_NAME: Final = 'FreeFlyBot.sqlite3'
#SQL_EXCEPT_VALUES: Final = (
#    'CREATE',
#    'UPDATE',
#    'DELETE',
#    'OR',
#    'AND',
#)
SQL_EXCEPT_CHARS: Final = (
    '"',
    '\'',
    ':',
    ';',
    '*'
)

SQL_TABLE_USERS: Final = 'users'
SQL_TABLE_SERVERS: Final = 'servers'
SQL_TABLE_TELE_GROUPS: Final = 'tele_groups'
SQL_TABLE_USER_BANS: Final = 'user_bans'

SQL_CREATE_TABLE_USERS: Final = f'''CREATE TABLE IF NOT EXISTS {SQL_TABLE_USERS} (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(15) NOT NULL UNIQUE);'''

SQL_CREATE_TABLE_SERVERS: Final = f'''CREATE TABLE IF NOT EXISTS {SQL_TABLE_SERVERS} (
    server_id INTEGER PRIMARY KEY);'''

SQL_CREATE_TABLE_TELE_GROUPS: Final = f'''CREATE TABLE IF NOT EXISTS {SQL_TABLE_TELE_GROUPS} (
    group_id INTEGER PRIMARY KEY);'''

SQL_CREATE_TABLE_USER_BANS: Final = f'''CREATE TABLE IF NOT EXISTS {SQL_TABLE_USER_BANS} (
    id INTEGER PRIMARY KEY,
    username VARCHAR(35) UNIQUE,
    reason VARCHAR(40));'''

# ! Bot
BOT_MAX_UPDATES: Final = 100
BOT_SLEEP_TIME_IN_SEC: Final = 1

BOT_PREFIX: Final = '/'

class BotCommands:
    HELP = "help"
    START = "start"
    TEST = "test"

BOT_TEST_GOODS = [
    [{'text': f'Конфера', 'callback_data': f'0'}],
    [{'text': f'Табак', 'callback_data': f'1'}],
    [{'text': f'Хлеб', 'callback_data': f'2'}],
    [{'text': f'Пивко', 'callback_data': f'3'}],
    [{'text': f'Вода', 'callback_data': f'4'}],
    [{"text": "Ввести текст", "switch_inline_query_current_chat": ""}],
]