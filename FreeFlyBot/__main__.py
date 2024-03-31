from sys import argv
from core import create_log, get_env, update_env
from sql import create_bd
from bot import Bot

from os.path import exists
from settings import SQL_BD_NAME


def main(args):
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
