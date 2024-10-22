import sqlite3
from core import create_log
from settings import (
    SQL_BD_NAME,
    CREATE_TABLE_EVENTS,
    CREATE_TABLE_SERVERS,
    CREATE_TABLE_TYPES,
    CREATE_TABLE_ON_JOIN,
    CREATE_TABLE_ON_JOIN_ACTIONS,
)


def create_bd():
    try:
        with sqlite3.connect(SQL_BD_NAME) as db:
            cursor = db.cursor()
            cursor.execute(CREATE_TABLE_EVENTS)
            db.commit()
            cursor.execute(CREATE_TABLE_SERVERS)
            db.commit()
            cursor.execute(CREATE_TABLE_TYPES)
            db.commit()
            cursor.execute(CREATE_TABLE_ON_JOIN)
            db.commit()
            cursor.execute(CREATE_TABLE_ON_JOIN_ACTIONS)
            db.commit()
            cursor.close()
    except sqlite3.Error as error:
        create_log(error, 'error')