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

async def db_check_type_for_exist(type_id: int) -> bool: #True если такая запись уже есть!!11
    async with aiosqlite.connect(SQL_BD_NAME) as db: 
        async with db.execute(f"""SELECT EXISTS (SELECT type_id FROM {TYPES_TABLE_NAME} WHERE type_id = {type_id});""") as cursor: 
            return True if list(await cursor.fetchall())[0][0] == 1 else False


async def db_delete_type(type_id: int):
    async with aiosqlite.connect(SQL_BD_NAME) as db:
        await db.execute(
            f'''DELETE FROM {TYPES_TABLE_NAME} WHERE type_id = {type_id};'''
        )
        await db.commit() 

async def db_types_list() -> list[EventType]:
    async with aiosqlite.connect(SQL_BD_NAME) as db:
        async with db.execute(f'''SELECT * FROM {TYPES_TABLE_NAME}''') as cursor:
            ret_list :list[EventType] = []
            async for row in cursor:
                ret_list.append(EventType(type_id= row[0], 
                                          server_id= row[1], 
                                          type_name= row[2], 
                                          channel_id= row[3], 
                                          role_id= row[4]
                                         ))
            return ret_list
        
async def db_get_type_by_id(type_id: int):
    async with aiosqlite.connect(SQL_BD_NAME)as db:
        event_query = f"""SELECT * FROM {TYPES_TABLE_NAME} WHERE type_id = {type_id}"""
        async with db.execute(event_query) as cursor:
            ret_server :EventType
            ret_server = None 
            async for row in cursor:
                ret_type = (EventType(type_id= row[0], 
                                        server_id= row[1], 
                                        type_name= row[2], 
                                        channel_id= row[3], 
                                        role_id= row[4]
                                         ))
        return ret_type
    

async def db_types_list_by_server_id(server_id: int) -> list[EventType]:
    async with aiosqlite.connect(SQL_BD_NAME) as db:
        async with db.execute(f'''SELECT * FROM {TYPES_TABLE_NAME} WHERE server_id = {server_id}''') as cursor:
            ret_list :list[EventType] = []
            async for row in cursor:
                ret_list.append(EventType(type_id= row[0], 
                                          server_id= row[1], 
                                          type_name= row[2], 
                                          channel_id= row[3], 
                                          role_id= row[4]
                                         ))
            return ret_list


async def db_get_type_by_name_and_server_id(server_id: int, type_name: str) -> EventType | None:
    async with aiosqlite.connect(SQL_BD_NAME)as db:
        event_query = f"""SELECT * FROM {TYPES_TABLE_NAME} WHERE server_id = {server_id} AND type_name = '{type_name}'"""
        async with db.execute(event_query) as cursor:
            ret_type :EventType 
            ret_type = None
            async for row in cursor:
                ret_type = (EventType(type_id= row[0], 
                                        server_id= row[1], 
                                        type_name= row[2], 
                                        channel_id= row[3], 
                                        role_id= row[4]
                                         ))
        return ret_type