import asyncio
from sys import argv
from core.debug import create_log
from bot.bot_main import Bot


def main(args: list):
    bot = Bot()
    asyncio.run(bot.get_updates())


if __name__ == "__main__":
    try:
        create_log(f'Run main: {argv}')
        main(argv[1:])
    except Exception as err:
        create_log(err, "crit")
