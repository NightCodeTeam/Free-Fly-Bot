import fastapi
import uvicorn
from core.debug import create_log
from core.dot_env import get_env
from bot_tele.bot_main import TeleBot
from threading import Thread
import asyncio


class ServerMain:
    def __init__(self):
        self.app = fastapi.FastAPI()
        self.bot_tele = TeleBot()
        Thread(target=self.run_bot, name='test').start()

    def run_bot(self):
        asyncio.run(self.bot_tele.run())

    async def run(self):
        #await self.bot_tele.run()
        create_log('Starting API')
        uvicorn.run(
            self.app,
            host=get_env('FASTAPI_HOST'),
            port=int(get_env('FASTAPI_PORT')),
            reload=True
        )