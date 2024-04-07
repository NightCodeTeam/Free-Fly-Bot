import aiosqlite
from core import create_log
from .data_classes import DiscordServer

from settings import (  # аыы не забудь воткнуть название таблицы!11
    DS_SERVERS_TABLE_NAME,
    SQL_BD_NAME,
)


async def db_add_server(data: DiscordServer) -> bool:
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            await db.execute(          # если поля названы не как в ТЗ все превратится в тыкву...
                f"""
                INSERT INTO {DS_SERVERS_TABLE_NAME} (server_id, server_name, server_sub) 
                VALUES ({data.server_id}, '{data.server_name}', {data.server_sub});
                """   
            )
            await db.commit()
            return True
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


async def db_check_server_for_exist(server_id: int) -> bool: #True если такая запись уже есть!!11
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db: #!!!!!эээ а почему у нас везде await db.execute а тут async with?!!?
            async with db.execute(f"""SELECT EXISTS (SELECT server_id FROM {DS_SERVERS_TABLE_NAME} WHERE server_id = {server_id});""") as cursor: 
                return True if list(await cursor.fetchall())[0][0] == 1 else False
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


async def db_delete_server(server_id: int) -> bool:
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            await db.execute(
                f'''DELETE FROM {DS_SERVERS_TABLE_NAME} WHERE server_id = {server_id};'''
            )
            await db.commit()
            return True
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


async def db_server_list() -> list[DiscordServer]:
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            async with db.execute(f'''SELECT * FROM {DS_SERVERS_TABLE_NAME}''') as cursor:
                ret_list: list[DiscordServer] = []
                async for row in cursor:
                    ret_list.append(DiscordServer(server_id= row[0], server_name= row[1], server_sub= row[2]))
                return ret_list
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return []


async def db_get_server_by_id(server_id: int) -> DiscordServer | None:
    try:
        async with aiosqlite.connect(SQL_BD_NAME)as db:
            event_query = f"""SELECT * FROM {DS_SERVERS_TABLE_NAME} WHERE server_id = {server_id}"""
            ret_server: DiscordServer | None = None 
            async with db.execute(event_query) as cursor:

                async for row in cursor:
                    ret_server = (DiscordServer(server_id= row[0], 
                                              server_name= row[1],
                                              server_sub= row[2] 
                                             ))
            return ret_server
    except aiosqlite.Error as err:
        create_log(err, 'error')
