import aiosqlite
from random import randint
from core import create_log
from .exceptions import SQLCantGetIDsException, SQLFullException


from settings import (
    SQL_BD_NAME,

    EVENTS_TABLE_NAME,
    TYPES_TABLE_NAME,
    ON_JOIN_TABLE_NAME,
    ON_JOIN_ACTIONS_TABLE_NAME,

    EVENTS_MIN_INDEX,
    EVENTS_MAX_INDEX,

    TYPES_MIN_INDEX,
    TYPES_MAX_INDEX,

    ON_JOIN_MIN_INDEX,
    ON_JOIN_MAX_INDEX,

    ON_JOIN_ACTIONS_MIN_INDEX,
    ON_JOIN_ACTIONS_MAX_INDEX,
)


async def db_get_ids(table: str) -> list:
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            cursor = await db.execute(
                f'''SELECT {'event_id' if table == EVENTS_TABLE_NAME else 'type_id'} FROM {table}'''
            )
            ans = []
            async for row in cursor:
                ans.append(row[0])
            return ans
    except aiosqlite.Error as err:
        create_log(err, 'error')
        raise SQLCantGetIDsException(table)


async def generate_id(table: str, min_index: int, max_index: int) -> int:
    table_ids = await db_get_ids(table)
    
    # ! Если id слишком много!
    if table == EVENTS_TABLE_NAME and len(table_ids) == EVENTS_MAX_INDEX:
        raise SQLFullException(table)
    if table == TYPES_TABLE_NAME and len(table_ids) == TYPES_MAX_INDEX:
        raise SQLFullException(table)
    
    while True:
        val = randint(min_index, max_index)
        if val not in table_ids:
            return val


async def db_create_event_id() -> int:
    return await generate_id(
        EVENTS_TABLE_NAME,
        EVENTS_MIN_INDEX,
        EVENTS_MAX_INDEX
    )


async def db_create_type_id() -> int:
    return await generate_id(
        TYPES_TABLE_NAME,
        TYPES_MIN_INDEX,
        TYPES_MAX_INDEX
    )


async def db_create_onjoin_id() -> int:
    return await generate_id(
        ON_JOIN_TABLE_NAME,
        ON_JOIN_MIN_INDEX,
        ON_JOIN_MAX_INDEX
    )


async def db_create_onjoin_action_id() -> int:
    return await generate_id(
        ON_JOIN_ACTIONS_TABLE_NAME,
        ON_JOIN_ACTIONS_MIN_INDEX,
        ON_JOIN_ACTIONS_MAX_INDEX
    )
