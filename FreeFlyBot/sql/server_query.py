import aiosqlite
#from random import randint
from data_classes import *

from settings import (  # аыы не забудь воткнуть название таблицы!11
    DS_SERVERS_TABLE_NAME,
    DB_NAME,
)

async def db_add_server(data: DiscordServer):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(          # если поля названы не как в ТЗ все превратится в тыкву...
            f"""
            INSERT INTO {DS_SERVERS_TABLE_NAME} (server_id, server_name) 
            VALUES ({data.server_id}, '{data.server_name}';
            """   
        )
        await db.commit()

async def db_check_for_exist (int: id):
    async with aiosqlite.connect(DB_NAME) as db:
         return await db.execute(f"""EXISTS (SELECT id FROM {DS_SERVERS_TABLE_NAME} WHERE server_id = {id})""")
