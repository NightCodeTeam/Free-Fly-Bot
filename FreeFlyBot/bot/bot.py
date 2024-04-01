from random import randint
import datetime
import discord
from typing import Any
from .exceptions import CallFuncBotNotInGuildException
from core import create_log
from sql import (
    Event,
    EventType,
    DiscordServer,

    db_add_event,
    db_get_events_by_type,
    db_delete_event,

    db_check_server_for_exist,
    db_add_server,

    db_add_type,
    db_check_type_for_exist,
    db_delete_type,
    db_types_list,
    db_get_type_by_id,

    db_get_type_by_id,
    db_types_list_by_server_id,
    db_get_type_by_name_and_server_id
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
    TOO_FEW_ARGS,
    TYPE_MSG,
    NO_TYPES_ON_SERVER,
    ADD_TYPE_ERROR_MSG,
    ADD_TYPE_ALREADY_EXISTS,
    DELETE_TYPE_NOT_FOUND,
    DELETE_TYPE_ALL_GOOD,
    EVENT_CANT_CREATE,
    DELETE_EVENT_ARGS_NULL,
    DELETE_EVENT_CANT_FIND,
    DELETE_EVENT_MSG,
)


class Bot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True  
        super().__init__(intents=intents)

    def __check_author_is_member(self, member) -> bool:
        return True if type(member) is discord.Member else False

    def __check_member_is_admin(self, member) -> bool:
        return True if member.guild_permissions.administrator else False

    async def __check_member_permisions(self, member, guild) -> bool:
        if self.__check_author_is_member(member):
            if (
                self.__check_member_is_admin(member) 
                or self.__check_member_has_reached_role(
                    member, await self.__get_server_types_roles_id(guild.id)
                )
            ):
                return True
        return False

    def __get_guilds_names(self) -> list[str]:
        return list(map(lambda x: x.name, list(self.guilds)))

    def __get_guilds_ids(self) -> list[int]:
        return list(map(lambda x: x.id, list(self.guilds)))
    
    def __get_channel(self, channel_id: str):
        return self.get_channel(int(channel_id[2:-1]))
    
    def __get_role(self, guild: discord.Guild, role_id: str):
        return discord.utils.get(guild.roles, id=int(role_id[3:-1]))
    
    async def __get_server_types(self, server_id: int) -> list[EventType]:
        return await db_types_list_by_server_id(server_id)
    
    async def __get_server_event_type_by_name(self, server_id: int, type_name: str) -> EventType | None:
        return await db_get_type_by_name_and_server_id(server_id, type_name)

    async def __get_server_types_roles_id(self, server_id) -> list[int]:
        return list(map(lambda x: x.role_id, await self.__get_server_types(server_id)))
    
    async def __get_server_types_names(self, server_id) -> list[str]:
        return list(map(lambda x: x.type_name, await self.__get_server_types(server_id)))
    
    def __check_member_has_reached_role(self, member, roles_id: list[int]) -> bool:
        if type(member) is discord.member.Member:
            for i in member.roles:
                if i.id in roles_id:
                    return True
        return False
    
    def __get_role_or_channel(self, guild: discord.Guild, arg: str) -> Any:
        """Возвращает 1 из 3:
        - Дискорд канал
        - Роль на сервере
        - None"""
        if arg.startswith('<#'):
            return self.__get_channel(arg)
        elif arg.startswith('<@&'):
            return self.__get_role(guild, arg)

    async def on_ready(self):
        for ids, names in zip(self.__get_guilds_ids(), self.__get_guilds_names()):
            if not await db_check_server_for_exist(ids):
                await db_add_server(DiscordServer(ids, names))

        create_log(f'Logged on as {self.user}!', 'info')

    async def on_message(self, message: discord.message.Message):
        #print(message.author, '>', message.content)
        if message.guild is None:
            print('Guild is None')
            return None
        if message.author != self.user and not message.author.bot:
            if message.content[0] == BOT_PREFIX:
                if await self.__check_member_permisions(message.author, message.guild):
                    pass
                else:
                    create_log(
                        f'Member {message.author} try to use bot but has no access',
                        'info'
                    )
                    return None
                args = message.content.split()
                create_log(f'Called parser {args[0]}', 'debug')
                match args[0][1:].lower():
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
        create_log(f"Help called with args: {args}", 'debug')
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
    
    # ! СОБЫТИЯ
    def __events_access_check(self, member, func_name: str) -> bool:
        return True

    async def events(self, message: discord.message.Message, *args):
        create_log(f"events called with args: {args}", 'debug')
        if not self.__events_access_check(message.author, 'events'):
            return None

    async def add_event(self, message: discord.message.Message, *args):
        if not self.__events_access_check(message.author, 'add_event'):
            return None

        message_str_list = message.content.split('\n')
        event_id = randint(0, 100)
        server_id = message.guild.id
        event_name = message_str_list[0].removeprefix('!addevent') # даем название
        type_id = await self.__get_server_event_type_by_name(message.guild.id, message_str_list[1])
        event_time = datetime.datetime.strptime(message_str_list[2], '%Y-%m-%d %H:%M')
        comment = ''
        if len(message_str_list) > 2:
            comment = '\n'.join(message_str_list[3:])
        
        if type_id is None or type(event_time) is not datetime.datetime:
            return await message.reply(EVENT_CANT_CREATE)

        event = Event(
            event_id,
            server_id,
            event_name,
            type_id.type_id,
            comment,
            event_time
        )

        await db_add_event(event)

    async def delete_event(self, message: discord.message.Message, *args):
        if not self.__events_access_check(message.author, 'add_event'):
            return None

        if len(args) == 0:
            return message.reply(DELETE_EVENT_ARGS_NULL)
        
        msg = ''
        # Находим id типов для этого сервера
        types_id = list(
            map(
                lambda x: x.type_id,
                await self.__get_server_types(message.guild.id)
            )
        )
        server_events = list(
            map(
                lambda x: x.event_id,
                await db_get_events_by_type(*types_id)
            )
        )

        for i in args:
            if i in server_events:
                await db_delete_event(int(i))
                msg += DELETE_EVENT_MSG.format(i)

        if msg == '':
            msg += DELETE_EVENT_CANT_FIND
        return await message.reply(msg)

    
    # ! Типы события
    def __types_access_check(self, member, func_name: str) -> bool:
        if not self.__check_member_is_admin(member):
            create_log(f"CANCEL {func_name}: member {member} is not admin")
            return False
        return True

    async def types(self, message: discord.message.Message, *args):
        create_log(f"types called with args: {args}", 'debug')
        if not self.__types_access_check(message.author, 'types'):
            return None
        msg = ''
        for i in await self.__get_server_types(message.guild.id):
            msg += TYPE_MSG.format(
                name=i.type_name,
                channel=self.get_channel(i.channel_id),
                role=self.__get_role(message.guild, str(i.role_id))
            )
        if msg == '':
            msg = NO_TYPES_ON_SERVER
        return await message.reply(msg)

    async def add_type(self, message: discord.message.Message, *args):
        create_log(f"add_type called with args: {args}", 'debug')
        if not self.__types_access_check(message.author, 'add_type'):
            return None
        if len(args) != 3:
            if len(args) > 3:
                return await message.reply(TOO_MANY_ARGS)
            elif len(args) < 3:
                return await message.reply(TOO_FEW_ARGS)
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

        if (
            type_name is None
            or type_channel_id is None
            or type_role_id is None
            or await db_get_type_by_name_and_server_id(message.guild.id, type_name) is not None
        ):
            return await message.reply(ADD_TYPE_ERROR_MSG)

        new_type = EventType(
            randint(0, 10),
            type_server_id,
            type_name,
            type_channel_id,
            type_role_id
        )
        await db_add_type(new_type)
    
    async def delete_type(self, message: discord.message.Message, *args):
        create_log(f"delete_type called with args: {args}", 'debug')
        if not self.__types_access_check(message.author, 'delete_type'):
            return None
        if len(args) == 0:
            return await message.reply(TOO_FEW_ARGS)
        server_types_names = await self.__get_server_types_names(message.guild.id)
        msg = ''
        for i in args:
            if i in server_types_names:
                eventtype = await self.__get_server_event_type_by_name(message.guild.id, i)
                if eventtype is not None:
                    await db_delete_type(eventtype.type_id)
                    create_log(f"Delete type {i}", 'debug')
                    msg += DELETE_TYPE_ALL_GOOD.format(i)
                else:
                    create_log(f"CANT delete type {i}", 'info')
                    msg += DELETE_TYPE_NOT_FOUND.format(i)
            else:
                msg += DELETE_TYPE_NOT_FOUND.format(i)
        return await message.reply(msg)