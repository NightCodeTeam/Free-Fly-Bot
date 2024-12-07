import fastapi
import uvicorn
from core.debug import create_log
from core.dot_env import get_env
from bot_tele.bot_main import TeleBot
from threading import Thread
import asyncio


class ServerMain:
    bot_tele: TeleBot

    def __init__(self):
        self.app = fastapi.FastAPI()

        self.thread = Thread(target=self.create_bot, name='test')
        self.thread.daemon = True
        self.thread.start()

    def create_bot(self):
        #loop = asyncio.new_event_loop()
        asyncio.run(self.run_bot())

    async def run_bot(self):
        self.bot_tele = TeleBot()
        await self.bot_tele.run()

    def run(self):
        #await self.bot_tele.run()
        create_log('Starting API')
        uvicorn.run(
            self.app,
            host=get_env('FASTAPI_HOST'),
            port=int(get_env('FASTAPI_PORT')),
        )