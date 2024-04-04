from sys import argv
from threading import Thread

from core import create_log, get_env, update_env, Timer
from sql import create_bd
from bot import Bot

from os.path import exists
from settings import SQL_BD_NAME


def main(args):
    #from datetime import datetime
    #print((datetime.now() - datetime(year=2024, month=5, day=30, hour=20, minute=20)).total_seconds())

    update_env()
    if not exists(SQL_BD_NAME):
        create_bd()
    bot = Bot()
    bot.run(get_env("BOT_TOKEN"))
    


if __name__ == "__main__":
    try:
        main(argv[1:])
    except Exception as err:
        create_log(err, "crit")
