import aiosqlite
#from random import randint
from .data_classes import *

from settings import (  # аыы не забудь воткнуть название таблицы!11
    DS_SERVERS_TABLE_NAME,
    SQL_BD_NAME,
)


async def db_add_server(data: DiscordServer):
    async with aiosqlite.connect(SQL_BD_NAME) as db:
        await db.execute(          # если поля названы не как в ТЗ все превратится в тыкву...
            f"""
            INSERT INTO {DS_SERVERS_TABLE_NAME} (server_id, server_name) 
            VALUES ({data.server_id}, '{data.server_name}');
            """   
        )
        await db.commit()
        

async def db_check_for_exist(server_id: int) -> bool:
    async with aiosqlite.connect(SQL_BD_NAME) as db:
        async with db.execute(f"""SELECT EXISTS (SELECT server_id FROM {DS_SERVERS_TABLE_NAME} WHERE server_id = {server_id});""") as cursor:
            return True if list(await cursor.fetchall())[0][0] == 1 else False
