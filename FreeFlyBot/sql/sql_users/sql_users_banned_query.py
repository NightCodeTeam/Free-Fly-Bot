import aiosqlite
from core.debug import create_log, call_log
from ..protected import sql_protected, sql_protected_async
from .sql_users_dataclass import UserBanned

from settings import (
    SQL_DATABASE_NAME,
    SQL_TABLE_USER_BANS
)


@call_log()
async def sql_get_banned_users() -> list[UserBanned]:
    try:
        async with aiosqlite.connect(SQL_DATABASE_NAME) as db:
            async with db.execute(f"SELECT * FROM {SQL_TABLE_USER_BANS};") as cursor:
                ans = []
                async for row in cursor:
                    ans.append(UserBanned(
                        id=row[0],
                        username=row[1],
                        reason=row[2]
                    ))
                return ans
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return ans


@sql_protected_async
@call_log()
async def sql_user_in_bans(user_id: int | None = None, user_name: str | None = None) -> bool:
    if user_id is None and user_name is None:
        create_log(f'sql_del_user_ban > no args', 'error')
        return False
    query = f"id={user_id}" if user_id is not None else f"username='{user_name}'"
    try:
        async with aiosqlite.connect(SQL_DATABASE_NAME) as db:
            async with db.execute(
                f"""SELECT EXISTS (SELECT id FROM {SQL_TABLE_USER_BANS} WHERE {query});"""
            ) as cursor:
                return True if list(await cursor.fetchall())[0][0] == 1 else False
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


@call_log()
@sql_protected_async
async def sql_add_user_ban(user: UserBanned) -> bool:
    try:
        async with aiosqlite.connect(SQL_DATABASE_NAME) as db:
            await db.execute(
                f"""INSERT INTO {SQL_TABLE_USER_BANS} (id, username, reason) 
                VALUES ({user.id}, '{user.username}', '{user.reason}');"""
            )
            await db.commit()
            return True
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False


@call_log()
@sql_protected_async
async def sql_del_user_ban(user_id: int | None = None, user_name: str | None = None) -> bool:
    if user_id is None and user_name is None:
        create_log(f'sql_del_user_ban > no args', 'error')
        return False
    query = f'id={user_id}' if user_id is not None else f"username='{user_name}'"
    try:
        async with aiosqlite.connect(SQL_DATABASE_NAME) as db:
            await db.execute(
                f"""DELETE FROM TABLE {SQL_TABLE_USER_BANS}
                WHERE {query};"""
            )
            await db.commit()
            return True
    except aiosqlite.Error as err:
        create_log(err, 'error')
        return False
