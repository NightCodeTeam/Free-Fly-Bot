import sqlite3
from core.debug import create_log
from core.filemanage import delete_file
from settings import (
    SQL_DATABASE_NAME,
    SQL_CREATE_TABLE_USERS,
    SQL_CREATE_TABLE_SERVERS,
    SQL_CREATE_TABLE_TELE_GROUPS,
    SQL_CREATE_TABLE_USER_BANS
)
import psutil

def get_process_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
        except psutil.NoSuchProcess:
            pass
        else:
            processes.append(pinfo)
    return processes

def create_bd():
    try:
        with sqlite3.connect(SQL_DATABASE_NAME) as db:
            cursor = db.cursor()
            
            # ! Все таблицы которые нужно создать
            #cursor.execute(SQL_CREATE_TABLE_USERS)
            #cursor.execute(SQL_CREATE_TABLE_SERVERS)
            #cursor.execute(SQL_CREATE_TABLE_TELE_GROUPS)
            cursor.execute(SQL_CREATE_TABLE_USER_BANS)
            
            db.commit()
            cursor.close()
    except sqlite3.Error as error:
        try:
            create_log('>>> Error in creating sql database', 'error')
            create_log(error, 'error')
            delete_file(SQL_DATABASE_NAME)
            exit(1)
        except PermissionError:
            print(get_process_info())
