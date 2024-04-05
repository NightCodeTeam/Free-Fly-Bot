import aiosqlite
from dataclasses import dataclass
from core import create_log

from settings import (
    SQL_BD_NAME,
    ON_JOIN_TABLE_NAME,
    ON_JOIN_ACTIONS_TABLE_NAME,
)


@dataclass
class OnJoin:
    onjoin_id: int
    server_id: int
    message: int
    channel_listen_id: int
    channel_admin_id: int


@dataclass
class OnJoinAction:
    action_id: int
    onjoin_id: int
    button_name: str
    button_color: str


async def db_add_onjoin(data: OnJoin) -> bool:
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            await db.execute(
                f"""
                INSERT INTO {ON_JOIN_TABLE_NAME} (onjoin_id, server_id, message, channel_listen_id, channel_admin_id) 
                VALUES ({data.onjoin_id}, {data.server_id},
                '{data.message}', {data.channel_listen_id}, 
                {data.channel_admin_id});   
                """   
            )
            await db.commit()
            return True
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


async def db_delete_onjoin(onjoin_id: int) -> bool:
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            await db.execute(
                f"""DELETE FROM {ON_JOIN_TABLE_NAME} WHERE onjoin_id = {onjoin_id};"""   
            )
            await db.commit()
            return True
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


async def db_get_onjoin(server_id: int) -> OnJoin | None:
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            async with db.execute(
                f"SELECT * FROM {ON_JOIN_TABLE_NAME} WHERE server_id = {server_id}"
            ) as cursor:
                ret_on_join: OnJoin | None = None
                async for row in cursor:
                    ret_on_join = OnJoin(
                        onjoin_id=row[0],
                        server_id=row[1],
                        message=row[2],
                        channel_listen_id=row[3],
                        channel_admin_id=row[4]
                    )
                return ret_on_join
    except aiosqlite.Error as err:
        create_log(err, 'error')


async def db_add_onjoin_action(data: OnJoinAction) -> bool:
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            await db.execute(
                f"""
                INSERT INTO {ON_JOIN_ACTIONS_TABLE_NAME} (action_id, onjoin_id, button_name, button_color) 
                VALUES ({data.action_id}, {data.onjoin_id},
                '{data.button_name}', '{data.button_color}');   
                """   
            )
            await db.commit()
            return True
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


async def db_delete_onjoin_action(onjoin_action_id: int) -> bool:
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            await db.execute(
                f"""DELETE FROM {ON_JOIN_ACTIONS_TABLE_NAME} WHERE action_id = {onjoin_action_id};"""   
            )
            await db.commit()
            return True
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


async def db_get_onjoin_actions(on_join_id: int) -> list[OnJoinAction]:
    try:
        async with aiosqlite.connect(SQL_BD_NAME) as db:
            async with db.execute(
                f"SELECT * FROM {ON_JOIN_ACTIONS_TABLE_NAME} WHERE onjoin_id = {on_join_id}"
            ) as cursor:
                ret_on_join: list[OnJoinAction] = []
                async for row in cursor:
                    ret_on_join.append(OnJoinAction(
                        action_id=row[0],
                        onjoin_id=row[1],
                        button_name=row[2],
                        button_color=row[3]
                    ))
                return ret_on_join
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return []
