import aiosqlite
from random import randint
from .data_classes import Event

from settings import (  # аыы не забудь воткнуть название таблицы!11
    EVENTS_TABLE_NAME,
    SQL_BD_NAME,
)

async def db_add_event(data: Event): #+++
    async with aiosqlite.connect(SQL_BD_NAME) as db:
        await db.execute(          # если поля названы не как в ТЗ все превратится в тыкву...
            f"""
            INSERT INTO {EVENTS_TABLE_NAME} (event_id, server_id, event_name, type_id, comment, event_time) 
            VALUES ({data.event_id}, {data.server_id},
            '{data.event_name}', {data.type_id}, 
            '{data.comment}', '{data.event_time}');   
            """   
        )
        await db.commit()


async def db_delete_event(event_id :int): #+++
    async with aiosqlite.connect(SQL_BD_NAME)as db:
        await db.execute(
            f"""DELETE FROM {EVENTS_TABLE_NAME} WHERE event_id = {event_id};"""    
        )
        await db.commit()


async def db_get_events_by_type(*args)-> list[Event]:
    async with aiosqlite.connect(SQL_BD_NAME)as db:
        event_query = f"""SELECT * FROM {EVENTS_TABLE_NAME} WHERE 0"""
        for i in args:
            event_query += f" OR type_id = {i}"
        event_query += ';'
        async with db.execute(event_query) as cursor:
            # вот тут надо попилить курсор...
            #print(cursor)
            ret_list :list[Event] = []
            async for row in cursor:
                ret_list.append(Event(event_id= row[0], 
                                      server_id= row[1], 
                                      event_name= row[2], 
                                      type_id= row[3], 
                                      comment= row[4],
                                      event_time= row[5]))
        return ret_list
    

async def db_get_events_list()-> list[Event]:
    async with aiosqlite.connect(SQL_BD_NAME)as db:
        event_query = f"""SELECT * FROM {EVENTS_TABLE_NAME}"""
        async with db.execute(event_query) as cursor:
            # вот тут надо попилить курсор...
            #print(cursor)
            ret_list :list[Event] = []
            async for row in cursor:
                ret_list.append(Event(event_id= row[0], 
                                      server_id= row[1], 
                                      event_name= row[2], 
                                      type_id= row[3], 
                                      comment= row[4],
                                      event_time= row[5]))
        return ret_list

  



