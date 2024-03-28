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
EVENTS_TABLE_NAME: Final = ""
TYPES_TABLE_NAME: Final = ""
DS_SERVERS_TABLE_NAME: Final = ""
PILOTS_TABLE_NAME: Final = ""
PILOT_ROLES_TABLE_NAME: Final = ""
DB_NAME: Final = ""
