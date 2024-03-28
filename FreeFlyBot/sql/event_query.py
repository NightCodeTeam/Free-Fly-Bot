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
            VALUES ({Event.event_id}, {Event.server_id},
            '{Event.event_name}', {Event.type_id}, 
            '{Event.comment}', '{Event.event_time}')   
            """   
        )
        await db.commit()



