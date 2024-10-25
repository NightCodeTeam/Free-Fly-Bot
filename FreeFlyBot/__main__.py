import asyncio
from sys import argv
from core.debug import create_log
#from api.fastapi_main import ServerMain
from bot_tele.bot_main import TeleBot


async def run_bots():

    print('start')
    bot = TeleBot()
    await bot.run()
    #server = ServerMain()
    #server.run()

def main(args: list):
    #server = ServerMain()
    #server.run()
    print('start????')
    asyncio.run(run_bots())


if __name__ == "__main__":
    try:
        create_log(f'Run main: {argv}')
        main(argv[1:])
    except Exception as err:
        create_log(err, "crit")
