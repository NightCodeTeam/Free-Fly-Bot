from core.debug import create_log
from .bot_dataclass import Update
from .bot_requests import HttpTeleBot
from settings import BOT_PREFIX, BotCommands
from text_messages import (
    START,
)
import asyncio


class TeleBot:
    def __init__(self):
        self.client = HttpTeleBot()

    async def run(self):
        while True:
            await self.get_updates()
            await asyncio.sleep(1)

    async def get_updates(self):
        # ! Главный метод отвечает за получение обновлений
        updates = await self.client.get_updates()
        for update in updates:
            print(f'>>> {update.message.user.username} > {update.message.text}')
            await self.client.sent_msg(update.message.chat.id, f'Получил: {update.message.text}')
            await self.parse_command(update)

    async def parse_command(self, update: Update):
        if update.message.text is not None and update.message.text.startswith(BOT_PREFIX):
            match update.message.text.split(' ')[0][1:]:
                case BotCommands.START | BotCommands.HELP:
                    await self.command_start(update)
                case _:
                    await self.command_not_found(update)

    async def command_not_found(self, update: Update):
        await self.client.sent_msg_reply(
            update.message.chat.id,
            f'Команда не найдена: {update.message.text.split(' ')[0]}\nИспользуйте команду /start чтобы узнать подробности',
            update.message.message_id
        )

    async def command_start(self, update: Update):
        await self.client.sent_msg_reply(
            update.message.chat.id,
            START,
            update.message.message_id
        )