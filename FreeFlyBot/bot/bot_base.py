from email import message
import discord
import asyncio
from typing import Any
from datetime import datetime
from core import create_log
from .bot_views import OnJoinView
from sql import (
    Event,
    EventType,
    DiscordServer,
    OnJoin,
    OnJoinAction,

    db_create_onjoin_id,
    db_get_onjoin,
    db_get_onjoin_actions,

    db_get_nearest_event,
    db_delete_event,
    db_get_type_by_id,

    db_check_server_for_exist,
    db_add_server,
    db_get_server_by_id,

    db_types_list_by_server_id,
    db_get_type_by_name_and_server_id,
)

from settings import (
    BotCommands,
    BOT_PREFIX,
)
from message_text import (
    TAX_PATING,
    HELP_MSG,
    HELP_COMMAND_NOT_FOUND,

    HELP_TYPES,
    HELP_ADD_TYPE,
    HELP_DELETE_TYPE,
    HELP_EVENTS,
    HELP_ADD_EVENT,
    HELP_DELETE_EVENT,

    EVENT_TIMER_MSG,
    ON_JOIN_ACTION_MSG,
)


class BotBase(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True  
        intents.members = True
        super().__init__(intents=intents)

    def check_author_is_member(self, member) -> bool:
        return True if type(member) is discord.Member else False

    def check_member_is_admin(self, member) -> bool:
        return True if member.guild_permissions.administrator else False

    async def check_member_permisions(self, member, guild) -> bool:
        if self.check_author_is_member(member):
            if (
                self.check_member_is_admin(member) 
                or self.__check_member_has_reached_role(
                    member, await self.get_server_types_roles_id(guild.id)
                )
            ):
                return True
        return False

    def __get_guilds_names(self) -> list[str]:
        return list(map(lambda x: x.name, list(self.guilds)))

    def __get_guilds_ids(self) -> list[int]:
        return list(map(lambda x: x.id, list(self.guilds)))
    
    async def get_server_types(self, server_id: int) -> list[EventType]:
        return await db_types_list_by_server_id(server_id)
    
    async def get_server_event_type_by_name(
        self,
        server_id: int,
        type_name: str
    ) -> EventType | None:
        return await db_get_type_by_name_and_server_id(server_id, type_name)

    async def get_server_types_roles_id(
        self,
        server_id: int
    ) -> list[int]:
        return list(
            map(
                lambda x: x.role_id,
                await self.get_server_types(server_id)
            )
        )
    
    async def get_server_types_names(
        self,
        server_id: int
    ) -> list[str]:
        return list(
            map(
                lambda x: x.type_name,
                await self.get_server_types(server_id)
            )
        )
    
    def __check_member_has_reached_role(
        self,
        member,
        roles_id: list[int]
    ) -> bool:
        if type(member) is discord.member.Member:
            return True if any(
                map(lambda x: x.id in roles_id, member.roles)
            ) else False
        return False

    def try_get_channel(self, channel_id: str):
        return self.get_channel(int(channel_id[2:-1]))
    
    def try_get_role(self, guild: discord.Guild, role_id: str):
        return discord.utils.get(guild.roles, id=int(role_id[3:-1]))
    
    def get_role_or_channel(self, guild: discord.Guild, arg: str) -> Any:
        """Возвращает 1 из 3:
        - Дискорд канал
        - Роль на сервере
        - None"""
        if arg.startswith('<#'):
            return self.try_get_channel(arg)
        elif arg.startswith('<@&'):
            return self.try_get_role(guild, arg)

    async def on_ready(self):
        for ids, names in zip(self.__get_guilds_ids(), self.__get_guilds_names()):
            if not await db_check_server_for_exist(ids):
                await db_add_server(DiscordServer(ids, names))

        create_log(f'Logged on as {self.user}', 'info')
        await self.timer()

    async def on_message(self, message: discord.message.Message):
        # Проверяем что все происходит на сервере а не в личке.
        if message.guild is None:
            create_log(f'Guild is None: {message.author}', 'info')
            return None
        if len(message.content) == 0:
            return None
        
        if not await db_get_server_by_id(message.guild.id).server_sub:
            await message.reply(TAX_PATING)
        
        if (
            not message.author.bot
            and message.content[0] == BOT_PREFIX
            # and message.author != self.user
        ):
            # Если у пользователя нет прав использовать бота.
            # Разрешенными является: админ и типы событий на сервере
            if not await self.check_member_permisions(
                message.author, message.guild
            ):
                create_log(
                    f'Member {message.author} try to use bot but has no access',
                    'info'
                )
                return None
            
            # Парсим аргументы
            args = message.content.split()
            match args[0][1:].lower():
                case BotCommands.BOT_HELP_PREFIX:
                    await self.help(message, *args[1:])
                case BotCommands.BOT_EVENTS_PREFIX:
                    await self.events(message, *args[1:])
                case BotCommands.BOT_ADD_EVENT_PREFIX:
                    await self.add_event(message)
                case BotCommands.BOT_DELETE_EVENT_PREFIX:
                    await self.delete_event(message, *args[1:])
                case BotCommands.BOT_TYPES_PREFIX:
                    await self.types(message, *args[1:])
                case BotCommands.BOT_ADD_TYPE_PREFIX:
                    await self.add_type(message, *args[1:])
                case BotCommands.BOT_DELETE_TYPE_PREFIX:
                    await self.delete_type(message, *args[1:])
                case BotCommands.ON_JOIN:
                    await self.on_join(message, *args[1:])
                case BotCommands.ON_JOIN_ACTIONS:
                    await self.on_join_actions(message, *args[1:])
                case BotCommands.ADD_ON_JOIN:
                    await self.add_on_join(message)
                case BotCommands.ADD_ON_JOIN_ACTIONS:
                    await self.add_on_join_action(message, *args[1:])
                case BotCommands.DEL_ON_JOIN:
                    await self.del_on_join(message, *args[1:])
                case BotCommands.DEL_ON_JOIN_ACTIONS:
                    await self.del_on_join_action(message, *args[1:])
                case 'test':
                    await self.test(message)
                case _:
                    await message.reply(HELP_COMMAND_NOT_FOUND.format(args[0]))

    async def timer(self):
        while True:
            nearest_event = await db_get_nearest_event()
            #print(nearest_event)
            if nearest_event is not None:
                #seconds = datetime.now() - nearest_event.event_time
                if (datetime.now() - nearest_event.event_time).total_seconds() >= -10:
                    create_log(f'Event run {nearest_event.event_id}', 'info')
                    #print(nearest_event.type_id)
                    typee = await db_get_type_by_id(nearest_event.type_id)
                    channel = self.get_channel(typee.channel_id)
                    #print(typee)
                    if typee is not None:
                        await self.send_msg(
                            typee.channel_id,
                            EVENT_TIMER_MSG.format(
                                role=discord.utils.get(channel.guild.roles, id=typee.role_id).mention,
                                name=nearest_event.event_name,
                                comment=nearest_event.comment
                            )
                        )
                        await db_delete_event(nearest_event.event_id)
                else:
                    #print(f'sleep: {(datetime.now() - nearest_event.event_time).total_seconds()}')
                    await asyncio.sleep(10)

    async def send_msg(self, channel_id: int, msg):
        # guild = self.get_guild(856825461685878797)
        channel = self.get_channel(channel_id)
        if channel is not None:
            await channel.send(
                msg
            )
    
    async def help(self, message: discord.message.Message, *args):
        create_log(f"Help called with args: {args}", 'debug')
        if len(args) == 0:
            return await message.reply(HELP_MSG)
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
    
    async def add_event(self, message: discord.message.Message):
        pass
    
    async def delete_event(self, message: discord.message.Message, *args):
        pass
    
    async def types(self, message: discord.message.Message, *args):
        pass
    
    async def add_type(self, message: discord.message.Message, *args):
        pass
    
    async def delete_type(self, message: discord.message.Message, *args):
        pass

    async def test(self, message: discord.message.Message):
        pass

    async def on_member_join(self, member: discord.member.Member):
        onjoin = await db_get_onjoin(member.guild.id)
        if onjoin is not None:
            actions = await db_get_onjoin_actions(onjoin.onjoin_id)
            channel_listen = self.get_channel(onjoin.channel_listen_id)
            view = OnJoinView(actions, member)
            await channel_listen.send(f'{member.mention} {onjoin.message}', view=view)
            if not await view.modal.wait():
                channel_admin = self.get_channel(onjoin.channel_admin_id)
                await channel_admin.send(
                    ON_JOIN_ACTION_MSG.format(
                        nick=member.mention,
                        name=view.user_name,
                        role=view.action_name,
                        msg=view.user_comment
                    )
                )

    # ! При присоединении
    async def on_join(self, msg: discord.message.Message):
        pass

    async def add_on_join(self, msg: discord.message.Message):
        pass

    async def del_on_join(self, msg: discord.message.Message):
        pass

    # ! Активности при присоединении
    async def on_join_actions(self, msg: discord.message.Message):
        pass

    async def add_on_join_action(self, msg: discord.message.Message, *args):
        pass

    async def del_on_join_action(self, msg: discord.message.Message, *args):
        pass