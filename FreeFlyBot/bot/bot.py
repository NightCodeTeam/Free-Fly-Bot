import discord
import datetime

from .bot_base import BotBase
from .bot_selectors import EventTypeSelector
from .bot_views import AddEventView
from core import create_log
from sql import (
    Event,
    EventType,
    DiscordServer,

    db_create_event_id,
    db_create_type_id,

    db_add_event,
    db_get_events_by_type,
    db_delete_event,

    db_add_type,
    db_check_type_for_exist,
    db_delete_type,
    db_types_list,
    db_get_type_by_id,

    db_get_type_by_id,
    db_types_list_by_server_id,
    db_get_type_by_name_and_server_id
)

from message_text import (
    TOO_MANY_ARGS,
    TOO_FEW_ARGS,
    TYPE_MSG,
    NO_TYPES_ON_SERVER,
    ADD_TYPE_MSG,
    ADD_TYPE_ERROR_MSG,
    ADD_TYPE_ALREADY_EXISTS,
    DELETE_TYPE_NOT_FOUND,
    DELETE_TYPE_MSG,
    EVENT_MSG,
    EVENT_NO_EVENTS_FOUND,
    ADD_EVENT_MSG,
    ADD_EVENT_CANT_CREATE,
    DELETE_EVENT_ARGS_NULL,
    DELETE_EVENT_CANT_FIND,
    DELETE_EVENT_MSG,
)


class Bot(BotBase):
    def __init__(self) -> None: 
        super().__init__()

    # ! СОБЫТИЯ
    def __events_access_check(self, member, func_name: str) -> bool:
        return True

    async def events(self, message: discord.message.Message, *args):
        create_log(f"events called with args: {args}", 'debug')
        # ? Проверяем допуск автора
        if not self.__events_access_check(message.author, 'events'):
            return None

        # Находим события сервера
        server_types_id = list(
            map(
                lambda x: x.type_id,
                await self.get_server_types(message.guild.id)
            )
        )
        server_events = await db_get_events_by_type(*server_types_id)
        
        msg = ''
        for i in server_events:
            msg += EVENT_MSG.format(
                event_id=i.event_id,
                name=i.event_name,
                date=i.event_time
            )
        
        if msg == '':
            msg += EVENT_NO_EVENTS_FOUND

        return await message.reply(msg)

    # ! Добавление события
    async def add_event(self, message: discord.message.Message):
        create_log(f"add_event called", 'debug')
        # ? Проверяем допуск автора
        if not self.__events_access_check(message.author, 'add_event'):
            return None

        # ! Костыль
        # Разбираем сообщение на строки
        message_str_list = message.content.split('\n')
        server_id = message.guild.id
        event_name = message_str_list[0].removeprefix('!addevent ') # даем название
        type_id = await self.get_server_event_type_by_name(
            message.guild.id,
            message_str_list[1]
        )
        event_time = datetime.datetime.strptime(
            message_str_list[2],
            '%Y-%m-%d %H:%M'
        )
        comment = ''
        if len(message_str_list) > 2:
            comment = '\n'.join(message_str_list[3:])

        # Проверки и создание типа
        if type_id is None or type(event_time) is not datetime.datetime:
            return await message.reply(EVENT_CANT_CREATE)

        # Отправляем в базу
        if await db_add_event(
            Event(
                await db_create_event_id(),
                server_id,
                event_name,
                type_id.type_id,
                comment,
                event_time
            )
        ):
            return await message.reply(ADD_EVENT_MSG.format(
                name=event_name,
                type=type_id.type_name,
                date=event_time
            ))
        else:
            return await message.reply(ADD_EVENT_CANT_CREATE)

    # ! Удаление события
    async def delete_event(self, message: discord.message.Message, *args):
        create_log(f"delete_event called with args: {args}", 'debug')
        # ? Проверяем допуск автора
        if not self.__events_access_check(message.author, 'delete_event'):
            return None

        # ? Проверка наличия аргументов
        if len(args) == 0:
            return message.reply(DELETE_EVENT_ARGS_NULL)
        
        # Находим id типов для этого сервера
        types_id = list(
            map(
                lambda x: x.type_id,
                await self.get_server_types(message.guild.id)
            )
        )
        server_events = list(
            map(
                lambda x: x.event_id,
                await db_get_events_by_type(*types_id)
            )
        )

        msg = ''
        if len(args) > 0:
            for i in args:
                if int(i) in server_events:
                    await db_delete_event(int(i))
                    msg += DELETE_EVENT_MSG.format(event_id=i)
        else:
            msg += DELETE_EVENT_CANT_FIND
        return await message.reply(msg)

    # ! Типы события
    def __types_access_check(self, member, func_name: str) -> bool:
        if not self.check_member_is_admin(member):
            create_log(f"CANCEL {func_name}: member {member} is not admin")
            return False
        return True

    async def types(self, message: discord.message.Message, *args):
        create_log(f"types called with args: {args}", 'debug')
        # ? Проверяем допуск автора
        if not self.__types_access_check(message.author, 'types'):
            return None

        msg = ''
        for i in await self.get_server_types(message.guild.id):
            msg += TYPE_MSG.format(
                name=i.type_name,
                channel=self.get_channel(i.channel_id),
                role=discord.utils.get(message.guild.roles, id=i.role_id).name
            )
        if msg == '':
            msg = NO_TYPES_ON_SERVER
        return await message.reply(msg)

    # ! Добавить тип события
    async def add_type(self, message: discord.message.Message, *args):
        create_log(f"add_type called with args: {args}", 'debug')
        # ? Проверяем допуск автора
        if not self.__types_access_check(message.author, 'add_type'):
            return None
        
        # Проверяем колличество аргументов
        if len(args) != 3:
            if len(args) > 3:
                return await message.reply(TOO_MANY_ARGS)
            elif len(args) < 3:
                return await message.reply(TOO_FEW_ARGS)
        
        # Создаем поля для класса
        type_name = None
        type_server_id = message.guild.id
        type_channel_id = None
        type_role_id = None
        for i in args:
            arg = self.get_role_or_channel(message.guild, i)
            if type(arg) is discord.channel.TextChannel:
                type_channel_id = arg.id
            elif type(arg) is discord.role.Role:
                type_role_id = arg.id
            else:
                type_name = i

        # Проверки
        if (
            type_name is None
            or type_channel_id is None
            or type_role_id is None
            or await db_get_type_by_name_and_server_id(message.guild.id, type_name) is not None
        ):
            return await message.reply(ADD_TYPE_ERROR_MSG)

        if await db_add_type(EventType(
            await db_create_type_id(),
            type_server_id,
            type_name,
            type_channel_id,
            type_role_id
        )):
            return message.reply(ADD_TYPE_MSG.format(type_name))
        else:
            return message.reply(ADD_TYPE_ERROR_MSG)
    
    # ! Удаление типа
    async def delete_type(self, message: discord.message.Message, *args):
        create_log(f"delete_type called with args: {args}", 'debug')
        # ? Проверяем допуск автора
        if not self.__types_access_check(message.author, 'delete_type'):
            return None

        # ! Удаление типа
        if len(args) == 0:
            return await message.reply(TOO_FEW_ARGS)
        
        server_types_names = await self.get_server_types_names(message.guild.id)
        
        msg = ''
        for i in args:
            if i in server_types_names:
                eventtype = await self.get_server_event_type_by_name(message.guild.id, i)
                if eventtype is not None:
                    await db_delete_type(eventtype.type_id)
                    create_log(f"Delete type {i}", 'debug')
                    msg += DELETE_TYPE_MSG.format(i)
                else:
                    create_log(f"CANT delete type {i}", 'info')
                    msg += DELETE_TYPE_NOT_FOUND.format(i)
            else:
                msg += DELETE_TYPE_NOT_FOUND.format(i)
        return await message.reply(msg)
    
    async def test(self, message: discord.message.Message, *args):
        types = await self.get_server_types(message.guild.id)
        view = AddEventView(types)

        await message.reply('Создайте событие:', view=view)
        
        if not await view.modal_ui.wait():
            await message.reply(f"Индекс события: {view.type_index}\nНазвание: {view.event_name}\nДата и время: {view.type_index} {view.event_time}\nКомментарий: {view.event_comment}")
        # TODO: Из вывода забрать то что написано и сделать класс Event и в бд
