from core.debug import create_log
from .bot_requests import HttpTeleBot
import asyncio


class TeleBot:
    def __init__(self):
        self.client = HttpTeleBot()
        self.last_update: int = 0

    async def run(self):
        while True:
            await self.get_updates()
            await asyncio.sleep(1)

    async def get_updates(self):
        updates = await self.client.get_updates(self.last_update)
        for update in updates:
            print(f'>>> {update.message.user.username} > {update.message.text}')
            self.last_update = update.update_id + 1
