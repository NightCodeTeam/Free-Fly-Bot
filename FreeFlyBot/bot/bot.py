from random import randint
import discord
from typing import Any
from .exceptions import CallFuncBotNotInGuildException
from sql import (
    Event,
    EventType,
    DiscordServer,

    db_check_server_for_exist,
    db_add_server,

    db_add_type,
    db_check_type_for_exist,
    db_delete_type,
    db_types_list,
    db_get_type_by_id,
)

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
    TOO_MANY_ARGS,
    ADD_TYPE_ERROR_MSG,
)


class Bot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True  
        super().__init__(intents=intents)

    def __get_guilds_names(self) -> list[str]:
        return list(map(lambda x: x.name, list(self.guilds)))

    def __get_guilds_ids(self) -> list[int]:
        return list(map(lambda x: x.id, list(self.guilds)))
    
    def __get_channel(self, channel_id: str):
        return self.get_channel(int(channel_id[2:-1]))
    
    def __get_role(self, guild: discord.Guild, role_id: str):
        return discord.utils.get(guild.roles, id=int(role_id[3:-1]))
    
    def __get_server_types(self, server_id: int) -> list[EventType]:
        return []

    def __get_server_types_roles(self, server_id) -> list[int]:
        return list(map(lambda x: x.role_id, self.__get_server_types(server_id)))
    
    def __get_role_or_channel(self, guild: discord.Guild, arg: str) -> Any:
        if arg.startswith('<#'):
            return self.__get_channel(arg)
        elif arg.startswith('<@&'):
            return self.__get_role(guild, arg)

    async def on_ready(self):
        for ids, names in zip(self.__get_guilds_ids(), self.__get_guilds_names()):
            if not await db_check_server_for_exist(ids):
                await db_add_server(DiscordServer(ids, names))

        print(f'Guilds: {self.__get_guilds_names()}\nLogged on as {self.user}!')

    async def on_message(self, message: discord.message.Message):
        if message.author != self.user and not message.author.bot:
            if type(message.author) is discord.Member:
                if message.author.guild_permissions.administrator:
                    print(f'{message.author} is admin')
                else:
                    print(f'{message.author} is not admin')
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

    async def send_msg(self, guild, channel, msg: str):
        pass
    
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
        #for i in args:
        #    print(self.__get_role(message.guild, i))
    
    async def add_type(self, message: discord.message.Message, *args):
        if message.guild is None:
            raise CallFuncBotNotInGuildException('add_type')
        if len(args) > 3:
            return await message.reply(TOO_MANY_ARGS)
        type_name = None
        type_server_id = message.guild.id
        type_channel_id = None
        type_role_id = None
        for i in args:
            arg = self.__get_role_or_channel(message.guild, i)
            if type(arg) is discord.channel.TextChannel:
                type_channel_id = arg.id
            elif type(arg) is discord.role.Role:
                type_role_id = arg.id
            else:
                type_name = i

        if type_name is None or type_channel_id is None or type_role_id is None:
            return await message.reply(ADD_TYPE_ERROR_MSG)

        new_type = EventType(
            randint(0, 10),
            type_server_id,
            type_name,
            type_channel_id,
            type_role_id
        )
        print(new_type) # TODO: Дописать вызов в базу и проверку на такой же тип
    
    async def delete_type(self, message: discord.message.Message, *args):
        pass
