import discord

from settings import (
    BotCommands,
    BOT_PREFIX,
)
from message_text import (
    HELP,
    HELP_TYPES,
    HELP_ADD_TYPE,
    HELP_DELETE_TYPE,
    HELP_EVENTS,
    HELP_ADD_EVENT,
    HELP_DELETE_EVENT,
    HELP_COMMAND_NOT_FOUND,
)


class Bot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True  
        super().__init__(intents=intents)

    def __get_guilds_names(self):
        return list(map(lambda x: x.name, list(self.guilds)))

    def __get_guilds_ids(self):
        return list(map(lambda x: x.id, list(self.guilds)))

    async def on_ready(self):
        print(f'Guilds: {self.__get_guilds_names()}\nLogged on as {self.user}!')

    async def on_message(self, message: discord.message.Message):
        if message.author != self.user and not message.author.bot:
            if message.content[0] == BOT_PREFIX:
                args = message.content.split()
                print(f'called parser {args[0]}')
                match args[0][1:]:
                    case BotCommands.BOT_HELP_PREFIX:
                        await self.help(message, *args[1:])
                    case BotCommands.BOT_EVENTS_PREFIX:
                        await self.events(message, *args[1:])
                    case BotCommands.BOT_ADD_EVENT_PREFIX:
                        await self.add_event(message, *args[1:])
                    case BotCommands.BOT_DELETE_EVENT_PREFIX:
                        await self.delete_event(message, *args[1:])
                    case BotCommands.BOT_TYPES_PREFIX:
                        await self.types(message, *args[1:])
                    case BotCommands.BOT_ADD_TYPE_PREFIX:
                        await self.add_type(message, *args[1:])
                    case BotCommands.BOT_DELETE_TYPE_PREFIX:
                        await self.delete_type(message, *args[1:])
                    case _:
                        await message.reply(HELP_COMMAND_NOT_FOUND.format(args[0]))
            else:
                print(f"{message.guild}\n{message.channel}\n{message.author}: {message.content}")
                #print(message.author.roles)
                #return await message.reply(message.content)
    
    async def help(self, message: discord.message.Message, *args):
        print(f"Help called with args: {args}")
        if len(args) == 0:
            return await message.reply(HELP)
        else:
            msg = ''
            for i in args:
                match i:
                    case BotCommands.BOT_EVENTS_PREFIX:
                        msg += HELP_EVENTS
                    case BotCommands.BOT_ADD_EVENT_PREFIX:
                        msg += HELP_ADD_EVENT
                    case BotCommands.BOT_DELETE_EVENT_PREFIX:
                        msg += HELP_DELETE_EVENT
                    case BotCommands.BOT_TYPES_PREFIX:
                        msg += HELP_TYPES
                    case BotCommands.BOT_ADD_TYPE_PREFIX:
                        msg += HELP_ADD_TYPE
                    case BotCommands.BOT_DELETE_TYPE_PREFIX:
                        msg += HELP_DELETE_TYPE
                    case _:
                        msg += HELP_COMMAND_NOT_FOUND.format(i)
            return await message.reply(msg)

    async def events(self, message: discord.message.Message, *args):
        pass
    
    async def add_event(self, message: discord.message.Message, *args):
        pass
    
    async def delete_event(self, message: discord.message.Message, *args):
        pass
    
    async def types(self, message: discord.message.Message, *args):
        pass
    
    async def add_type(self, message: discord.message.Message, *args):
        pass
    
    async def delete_type(self, message: discord.message.Message, *args):
        pass
