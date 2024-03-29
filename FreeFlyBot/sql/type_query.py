import aiosqlite
from random import randint
from .data_classes import EventType

from settings import (  # аыы не забудь воткнуть название таблицы!11
    TYPES_TABLE_NAME,
    SQL_BD_NAME,
)



async def db_add_type(data: EventType):               #это работает, к стати, фани факт, ему в принципе вообще поебать 
    async with aiosqlite.connect(SQL_BD_NAME) as db:  #ссылаюсь я на реальный server_id или нет...
        await db.execute(
            f"""
            INSERT INTO {TYPES_TABLE_NAME} (type_id, server_id, type_name, channel_id, role_id) 
            VALUES ({data.type_id}, {data.server_id}, '{data.type_name}', {data.channel_id}, {data.role_id});
            """   
        )
        await db.commit()

async def db_delete_type(type_id :int): # это тоже не работает
    async with aiosqlite.connect(SQL_BD_NAME)as db:
        await db.execute(
            f"""DELETE FROM {TYPES_TABLE_NAME} WHERE type_id = {type_id};"""    
        )
        await db.commit()

async def db_get_types() -> list[EventType]: # это тоже не работает
    async with aiosqlite.connect(SQL_BD_NAME)as db:
        await db.execute(
            f"""DELETE FROM {TYPES_TABLE_NAME} WHERE type_id = {type_id};"""    
        )
        await db.commit()