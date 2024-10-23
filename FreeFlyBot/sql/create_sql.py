import sqlite3
from core.debug import create_log
from core.filemanage import delete_file
from settings import (
    SQL_DATABASE_NAME,
    SQL_CREATE_TABLE_USERS,
    SQL_CREATE_TABLE_SERVERS,
    SQL_CREATE_TABLE_TELE_GROUPS,
    SQL_CREATE_TABLE_IP_BANS
)


def create_bd():
    try:
        with sqlite3.connect(SQL_DATABASE_NAME) as db:
            cursor = db.cursor()
            
            # ! Все таблицы которые нужно создать
            cursor.execute(SQL_CREATE_TABLE_USERS)
            #cursor.execute(SQL_CREATE_TABLE_SERVERS)
            #cursor.execute(SQL_CREATE_TABLE_TELE_GROUPS)
            #cursor.execute(SQL_CREATE_TABLE_IP_BANS)
            
            db.commit()
            cursor.close()
    except sqlite3.Error as error:
        create_log('>>> Error in creating sql database', 'error')
        create_log(error, 'error')
        delete_file(SQL_DATABASE_NAME)
        exit(1)
