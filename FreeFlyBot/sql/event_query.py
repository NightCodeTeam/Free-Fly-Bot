import aiosqlite
from core import create_log
from .data_classes import Event

from settings import (  # аыы не забудь воткнуть название таблицы!11
    EVENTS_TABLE_NAME,
    SQL_BD_NAME,
)


async def db_add_event(data: Event) -> bool:
    try:
        print(data)
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            await db.execute(          # если поля названы не как в ТЗ все превратится в тыкву...
                f"""
                INSERT INTO {EVENTS_TABLE_NAME} (event_id, server_id, event_name, type_id, comment, event_time) 
                VALUES ({data.event_id}, {data.server_id},
                '{data.event_name}', {data.type_id}, 
                '{data.comment}', '{data.event_time}', '{data.event_extra_time}');   
                """   
            )
            await db.commit()
            return True
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


async def db_delete_event(event_id: int) -> bool:
    try:
        async with aiosqlite.connect(SQL_BD_NAME)as db:
            await db.execute(
                f"""DELETE FROM {EVENTS_TABLE_NAME} WHERE event_id = {event_id};"""    
            )
            await db.commit()
            return True
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


async def db_get_events_by_type(*args) -> list[Event]:
    try:
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
                    ret_list.append(
                        Event(
                            event_id= row[0], 
                            server_id= row[1], 
                            event_name= row[2], 
                            type_id= row[3], 
                            comment= row[4],
                            event_time= row[5],
                            event_extra_time= row[6]
                        )
                    )
            return ret_list
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return []


async def db_get_events_list() -> list[Event]:
    try:
        async with aiosqlite.connect(SQL_BD_NAME)as db:
            event_query = f"""SELECT * FROM {EVENTS_TABLE_NAME}"""
            async with db.execute(event_query) as cursor:
                ret_list :list[Event] = []
                async for row in cursor:
                    ret_list.append(
                        Event(
                            event_id= row[0], 
                            server_id= row[1], 
                            event_name= row[2], 
                            type_id= row[3], 
                            comment= row[4],
                            event_time= row[5],
                            event_extra_time= row[6]
                        )
                    )
            return ret_list
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return []


async def db_check_event_for_exist(event_id: int) -> bool:
    try: #True если такая запись уже есть!!11
        async with aiosqlite.connect(SQL_BD_NAME) as db: 
            async with db.execute(f"""SELECT EXISTS (SELECT event_id FROM {EVENTS_TABLE_NAME} WHERE event_id = {event_id});""") as cursor: 
                return True if list(await cursor.fetchall())[0][0] == 1 else False
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


async def db_get_event_by_id(event_id: int) -> Event | None:
    try:
        async with aiosqlite.connect(SQL_BD_NAME)as db:
            event_query = f"""SELECT * FROM {EVENTS_TABLE_NAME} WHERE event_id = {event_id}"""
            ret_event: Event | None = None
            async with db.execute(event_query) as cursor:
                async for row in cursor:
                    ret_event = (
                        Event(
                            event_id= row[0], 
                            server_id= row[1], 
                            event_name= row[2], 
                            type_id= row[3], 
                            comment= row[4],
                            event_time= row[5],
                            event_extra_time= row[6]
                        )
                    )
            return ret_event
    except aiosqlite.Error as err:
        create_log(err, 'error')


async def db_get_nearest_event() -> Event | None:
    try:
        async with aiosqlite.connect(SQL_BD_NAME)as db:
            event_query = f"""SELECT * FROM {EVENTS_TABLE_NAME} ORDER BY event_time LIMIT 1"""
            ret_event: Event | None = None
            async with db.execute(event_query) as cursor:
                async for row in cursor:
                    ret_event = (
                        Event(
                            event_id= row[0], 
                            server_id= row[1], 
                            event_name= row[2], 
                            type_id= row[3], 
                            comment= row[4],
                            event_time= row[5],
                            event_extra_time= row[6]
                        )
                    )
            return ret_event
    except aiosqlite.Error as err:
        create_log(err, 'error')
