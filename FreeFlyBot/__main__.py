from sys import argv
from core import create_log, get_env, update_env
from bot import Bot


def main(args):
    update_env()
    bot = Bot()
    bot.run(get_env("BOT_TOKEN"))
    #bot.run(get_env("BOT_TOKEN"))


if __name__ == "__main__":
    try:
        main(argv[1:])
    except Exception as err:
        create_log(err, "crit")
