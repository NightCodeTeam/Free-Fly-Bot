from typing import Final


# ! DEBUG
DEBUG: Final = True
LOGGER_LEVEL: Final = 'debug'
MAIN_LOGGER: Final = 'logger'
MAIN_LOGGER_MAX_BITES: Final = 1_000_000
ERROR_LOGGER: Final = 'error'

# ! Основа
ENV_FILE: Final = '.env'
FOLDER_FILES: Final = 'data'

# ! SQL
SQL_DATABASE_NAME: Final = 'db.sqlite3'
SQL_EXCEPT_VALUES: Final = (
    'CREATE',
    'UPDATE',
    'DELETE',
    'OR',
    'AND',
)
SQL_EXCEPT_CHARS: Final = (
    '"',
    '\'',
    ':',
    ';',
)

SQL_TABLE_USERS: Final = 'users'
SQL_TABLE_SERVERS: Final = 'servers'
SQL_TABLE_TELE_GROUPS: Final = 'tele_groups'
SQL_TABLE_IP_BANS: Final = 'ip_bans'

SQL_CREATE_TABLE_USERS: Final = f'''CREATE TABLE IF NOT EXISTS {SQL_TABLE_USERS} (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(15) NOT NULL UNIQUE);'''

SQL_CREATE_TABLE_SERVERS: Final = f'''CREATE TABLE IF NOT EXISTS {SQL_TABLE_SERVERS} (
    server_id INTEGER PRIMARY KEY);'''

SQL_CREATE_TABLE_TELE_GROUPS: Final = f'''CREATE TABLE IF NOT EXISTS {SQL_TABLE_TELE_GROUPS} (
    group_id INTEGER PRIMARY KEY);'''

SQL_CREATE_TABLE_IP_BANS: Final = f'''CREATE TABLE IF NOT EXISTS {SQL_TABLE_IP_BANS} (
    user_id INTEGER PRIMARY KEY,
    reason VARCHAR(30);'''