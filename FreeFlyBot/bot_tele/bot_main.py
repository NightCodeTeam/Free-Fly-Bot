from core.debug import create_log
from .bot_requests import HttpTeleBot
import asyncio


class TeleBot:
    def __init__(self):
        self.client = HttpTeleBot()

    async def run(self):
        while True:
            await self.get_updates()
            await asyncio.sleep(1)

    async def get_updates(self):
        updates = await self.client.get_updates()
        for update in updates:
            print(f'>>> {update.message.user.username} > {update.message.text}')
