import discord
import datetime

from .bot_base import BotBase
from .bot_selectors import EventTypeSelector
from .bot_views import AddEventView
from core import create_log
from sql import (
    Event,
    EventType,

    db_create_type_id,

    db_add_event,
    db_get_events_by_type,
    db_delete_event,

    db_add_type,
    db_delete_type,
    db_get_type_by_id,

    db_get_type_by_id,
    db_get_type_by_name_and_server_id,

    OnJoin,
    OnJoinAction,
    db_create_onjoin_id,
    db_create_onjoin_action_id,
    db_get_onjoin,
    db_get_onjoin_actions,
    db_add_onjoin,
    db_add_onjoin_action,
    db_delete_onjoin,
    db_delete_onjoin_action,
)

from settings import ACTIONS_COLORS

from message_text import (
    TOO_MANY_ARGS,
    TOO_FEW_ARGS,
    TYPE_MSG,
    NO_TYPES_ON_SERVER,
    NO_PERMITTED_TYPES,
    ADD_TYPE_MSG,
    ADD_TYPE_ERROR_MSG,
    DELETE_TYPE_NOT_FOUND,
    DELETE_TYPE_MSG,
    EVENT_MSG,
    EVENT_NO_EVENTS_FOUND,
    ADD_EVENT_MSG,
    ADD_EVENT_CANT_CREATE,
    DELETE_EVENT_ARGS_NULL,
    DELETE_EVENT_CANT_FIND,
    DELETE_EVENT_MSG,

    ON_JOIN_ACTION_MSG,

    ON_JOIN_MSG,
    ON_JOIN_CANT_CREATE,
    ON_JOIN_NOT_FOUND,

    ON_JOIN_ACTIONS_MSG,
    ON_JOIN_ACTION_CANT_CREATE,
    ON_JOIN_ACTIONS_NOT_FOUND,

    ON_JOIN_ADD_MSG,
    ON_JOIN_ADD_CANT_CREATE,

    ON_JOIN_DEL_MSG,
    ON_JOIN_DEL_CANT_CREATE,

    ON_JOIN_ACTION_DEL,
    EVENT_TIMER_MSG,
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
            if (event_type.role_id in role_list) or(self.check_member_is_admin(member)):
                ret_events.append(i)
        create_log('For member {member} events: {ret_events}')
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
        if len(types) == 0:
            return await message.reply(NO_TYPES_ON_SERVER)
        if not self.check_member_is_admin(message.author):
            for i in types:
                if i.role_id not in list(map(lambda x: x.id, message.author.roles)):
                    types.remove(i)

        if len(types) == 0:
            return await message.reply(NO_PERMITTED_TYPES)

        view = AddEventView(message.guild, types, message.author)
        
        await message.reply('Создайте событие:', view=view)
        
        if not await view.modal_ui.wait():
            # а вот тут мы его проверяем
            # if len(self.__events_access_check(message.author, [view.event])) == 0:
            #     return await message.reply(ADD_EVENT_CANT_CREATE) # на свой вкус алерт воткни))
            
            # Отправляем в базу
            if view.event is not None:
                if await db_add_event(view.event):
                    typee = await db_get_type_by_id(view.type_index)
                    if typee is None:
                        view = None
                        return await message.reply(ADD_EVENT_CANT_CREATE)  
                    typee = await db_get_type_by_id(view.event.type_id)  
                    channel = self.get_channel(typee.channel_id)  #тут мы посылаем пинг в свой канал как в таймере... 
                    guild = channel.guild
                    role = guild.get_role(typee.role_id)   
                    await self.send_msg(typee.channel_id,
                                        EVENT_TIMER_MSG.format(
                                            role=role.mention if ((role.mention is not None)and(str(role) != '@everyone')) else role,
                                            name=view.event.event_name,
                                            time=view.event.event_time.strftime('%Y-%m-%d %H:%M'),
                                            comment=view.event.comment
                                        )
                                    )
                    #await message.reply(ADD_EVENT_MSG.format( это то что было, на всякий случай
                    #    name=view.event.event_name,
                    #    type=typee.type_name,
                    #    date=view.event.event_time
                    #))
                    view = None
                    return None
        view = None
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
                await self.__events_access_check(message.author, await db_get_events_by_type(*types_id))
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
            elif arg == '@everyone':
                type_role_id = arg
            else:
                type_name = i

        # Проверки
        if (
            type_name is None
            or type_channel_id is None
            or type_role_id is None
            or await db_get_type_by_name_and_server_id(message.guild.id, type_name) is not None
        ):
            #print(type_role_id, type_name)
            return await message.reply(ADD_TYPE_ERROR_MSG)

        try:
            typee = EventType(
                await db_create_type_id(),
                type_server_id,
                type_name,
                type_channel_id,
                type_role_id
            )
            await db_add_type(typee)
            return await message.reply(ADD_TYPE_MSG.format(typee.type_name))
        except Exception:
            return await message.reply(ADD_TYPE_ERROR_MSG)
    
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

    # ! События присоединения учасника
    async def on_join(self, msg: discord.message.Message):
        if not self.__types_access_check(msg.author, 'on_join'):
            return None
        onjoin = await db_get_onjoin(msg.guild.id)
        if onjoin is not None:
            await msg.reply(ON_JOIN_MSG.format(
                message=onjoin.message,
                channel_listen=self.get_channel(onjoin.channel_listen_id).mention,
                channel_admin=self.get_channel(onjoin.channel_admin_id).mention
            ))
        else:
            await msg.reply(ON_JOIN_NOT_FOUND)

    async def add_on_join(self, msg: discord.message.Message):
        if not self.__types_access_check(msg.author, 'add_on_join'):
            return None
        if await db_get_onjoin(msg.guild.id) is not None:
            return None
        try:
            msg_list = msg.content.split('\n')
            onjoin = OnJoin(
                await db_create_onjoin_id(),
                msg.guild.id,
                msg_list[3],
                self.try_get_channel(msg_list[1].split()[0]).id,
                self.try_get_channel(msg_list[2].split()[0]).id
            )
            if await db_add_onjoin(onjoin):
                await msg.reply(ON_JOIN_ADD_MSG)
        except Exception as err:
            create_log(err, 'error')
            await msg.reply(ON_JOIN_ADD_CANT_CREATE)

    async def del_on_join(self, msg: discord.message.Message):
        if not self.__types_access_check(msg.author, 'del_on_join'):
            return None
        onjoin = await db_get_onjoin(msg.guild.id)
        if onjoin is not None:
            await db_delete_onjoin(onjoin.onjoin_id)
            await msg.reply(ON_JOIN_DEL_MSG)
        else:
            await msg.reply(ON_JOIN_DEL_CANT_CREATE)

    # ! Активности при присоединении
    async def on_join_actions(self, msg: discord.message.Message):
        if not self.__types_access_check(msg.author, 'on_join_actions'):
            return None
        onjoin = await db_get_onjoin(msg.guild.id)
        if onjoin is not None:
            actions = await db_get_onjoin_actions(onjoin.onjoin_id)
            answer = ''
            if len(actions) != 0:
                for i in actions:
                    answer += ON_JOIN_ACTIONS_MSG.format(
                        aid=i.action_id,
                        name=i.button_name,
                        color=i.button_color
                    )
                await msg.reply(answer)
            else:
                await msg.reply(ON_JOIN_ACTIONS_NOT_FOUND)

    async def add_on_join_action(self, msg: discord.message.Message, *args):
        create_log(f'Add action called with args: {args}')
        if not self.__types_access_check(msg.author, 'add_on_join_action'):
            return None
        if args[1] not in ACTIONS_COLORS:
            return None
        onjoin = await db_get_onjoin(msg.guild.id)
        if onjoin is not None:
            try:
                action = OnJoinAction(
                    await db_create_onjoin_action_id(),
                    onjoin.onjoin_id,
                    args[0],
                    args[1],
                    args[2]
                )
                await db_add_onjoin_action(action)
                return await msg.reply(ON_JOIN_ACTIONS_MSG.format(
                    aid=action.action_id,
                    name=action.button_name,
                    color=action.button_color
                ))
            except Exception as err:
                create_log(err, 'error')
                return await msg.reply(ON_JOIN_ACTION_CANT_CREATE)

    async def del_on_join_action(self, msg: discord.message.Message, *args):
        if not self.__types_access_check(msg.author, 'del_on_join_action'):
            return None
        onjoin = await db_get_onjoin(msg.guild.id)
        if onjoin is not None:
            answer = ''
            actions_id = list(
                map(
                    lambda x: x.action_id,
                    await db_get_onjoin_actions(onjoin.onjoin_id)
                )
            )
            for i in args:
                if int(i) in actions_id:
                    await db_delete_onjoin_action(int(i))
                    answer += ON_JOIN_ACTION_DEL.format(id=i)
            if answer == '':
                answer = 'Не удалось'
            await msg.reply(answer)

    async def test(self, message: discord.message.Message, *args):
        pass
        #print(message.guild.default_role)
