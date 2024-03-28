import aiosqlite
from random import randint
from data_classes import *

from settings import (  # аыы не забудь воткнуть название таблицы!11
    EVENTS,
    DB_NAME,
)

async def db_add_event(data: Event):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(          # если поля названы не как в ТЗ все превратится в тыкву...
            f"""
            INSERT INTO {EVENTS} (event_id, server_id, event_name, type_id, comment, event_time) 
            VALUES ({data.event_id}, {data.server_id},
            '{data.event_name}', {data.type_id}, 
            '{data.comment}', '{data.event_time}');   
            """   
        )
        await db.commit()

async def db_delete_event(event_id :int):
    async with aiosqlite.connect(DB_NAME)as db:
        await db.execute(
            f"""DELETE FROM {EVENTS} WHERE event_id = {event_id};"""    
        )
        await db.commit()



