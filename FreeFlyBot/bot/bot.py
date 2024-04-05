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
    db_get_event_by_id,

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
    async def __events_access_check(self, member, events: list[Event]) -> list[Event]:
        ret_events: list[Event] = []
        role_list  = list(map(lambda x: x.id, member.roles))# сптсок роль айда у пользователя
        for i in events:
            event_type = await db_get_type_by_id(i.type_id)
            if event_type.role_id in role_list:
                ret_events.append(i)
        return ret_events

    async def events(self, message: discord.message.Message, *args):
        create_log(f"events called with args: {args}", 'debug')
        # ? Проверяем допуск автора
        #if not self.__events_access_check(message.author, 'events'):
         #   return None

        # Находим события сервера
        server_types_id = list(
            map(
                lambda x: x.type_id,
                await self.get_server_types(message.guild.id)
            )
        )
        role_list  = list(map(lambda x: x.id, message.author.roles))

        ###message.author.get_role
        server_events = await db_get_events_by_type(*server_types_id)
        access_server_events = await self.__events_access_check(message.author, server_events)
        #for i in server_events:
        #    if i.type_id not in role_list:
        #        server_events.remove(i)
        msg = ''
        for i in access_server_events:
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
        # ! Костыль
        # Разбираем сообщение на строки
        types = await self.get_server_types(message.guild.id)
        for i in types:
            if i not in message.author.roles:
                types.remove(i)
        view = AddEventView(types, message.author)

        await message.reply('Создайте событие:', view=view)
        
        if not await view.modal_ui.wait():
            # а вот тут мы его проверяем
            # if len(self.__events_access_check(message.author, [view.event])) == 0:
            #     return await message.reply(ADD_EVENT_CANT_CREATE) # на свой вкус алерт воткни))
            
            # Отправляем в базу
            if view.event is not None:
                #print('event good')
                if await db_add_event(view.event):
                    return await message.reply(ADD_EVENT_MSG.format(
                        name=view.event.event_name,
                        type=view.type_index,
                        date=view.event.event_time
                    ))
                else:
                    return await message.reply(ADD_EVENT_CANT_CREATE)
        return await message.reply(ADD_EVENT_CANT_CREATE)

    # ! Удаление события
    async def delete_event(self, message: discord.message.Message, *args):
        create_log(f"delete_event called with args: {args}", 'debug')
        # ? Проверяем допуск автора
        #if not self.__events_access_check(message.author, 'delete_event'):
        #    return None

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
                self.__events_access_check(message.author, await db_get_events_by_type(*types_id))
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
        pass