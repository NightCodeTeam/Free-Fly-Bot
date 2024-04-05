from typing import Final
from settings import (
    BOT_PREFIX,
    BotCommands,
)


HELP_MSG: Final = f'''Привет! Это бот для создания и отслеживания событий.\
 Для начала работы мне нужно настроить тип события:
- {BOT_PREFIX}{BotCommands.BOT_TYPES_PREFIX} - все типы на сервере
- {BOT_PREFIX}{BotCommands.BOT_ADD_TYPE_PREFIX} - добавить тип
- {BOT_PREFIX}{BotCommands.BOT_DELETE_TYPE_PREFIX} - удалить тип

Вот мои команды:
- {BOT_PREFIX}{BotCommands.BOT_EVENTS_PREFIX} - список всех событий
- {BOT_PREFIX}{BotCommands.BOT_ADD_EVENT_PREFIX} - добавить событие
- {BOT_PREFIX}{BotCommands.BOT_DELETE_EVENT_PREFIX} - удалить событие
'''

# ! Сообщения
ON_JOIN_ACTION_MSG: Final = 'Ник: {nick}\nХочет получить роль **{role}**\nОбращаться: {name}\nДоп сообщение: {msg}'

HELP_TYPES: Final = f'''Команда {BotCommands.BOT_TYPES_PREFIX}\n'''

HELP_ADD_TYPE: Final = f'''Команда {BotCommands.BOT_ADD_TYPE_PREFIX} добавляет новые типы событий на сервере.\
Чтобы это сделать вам нужно:
- указать удобное вам название (например test)
- роль которая может создавать события и которые будут пинговаться (например @test)
- канал в котором будут пинговаться события (например #test)'''
HELP_DELETE_TYPE: Final = f'''Команда {BotCommands.BOT_DELETE_TYPE_PREFIX} удаляет тип события для этого \
укажите её название (например test). \
Можно так же указывать несколько через пробел(test1 test2 test3)'''
HELP_EVENTS: Final = f'''Команда {BotCommands.BOT_EVENTS_PREFIX} показывает все ожидаемые с ролью участника \
события. Дополнительно в аргументах можно указать тип события, а так же \
администраторам можно воспользоваться типом all - покажет все события на сервере.'''
HELP_ADD_EVENT: Final = f'''Команда {BotCommands.BOT_ADD_EVENT_PREFIX} создает событие. Для этого нужно указать:
- Название
- Тип события
- дату
- комментарии'''
HELP_DELETE_EVENT: Final = f'''Команда {BotCommands.BOT_DELETE_EVENT_PREFIX} - удаляет событые. В качестве аргумента укажите номер события.'''

HELP_COMMAND_NOT_FOUND: Final = '''Команда {} не найдена. Используейте !help для выводы всех команд\n'''


TYPE_MSG: Final = '''Тип: {name} Канал: {channel} Роль: {role}\n'''
NO_TYPES_ON_SERVER: Final = '''Еще небыли созданы типы событий, используйте команду !addtype'''

ADD_TYPE_MSG: Final = '''Тип {} создан!'''
ADD_TYPE_ERROR_MSG: Final = '''Мне не удалось создать тип, проверьте правильность и попробуйте снова'''
ADD_TYPE_ALREADY_EXISTS: Final = '''Вы пытаетесь добавить тип с названием {}, но он уже существует'''

DELETE_TYPE_MSG: Final = '''Тип {} удален\n'''
DELETE_TYPE_NOT_FOUND: Final = '''Не удалось найти указанный тип: {}\n'''

EVENT_MSG: Final = '''Событие: {event_id} Название: {name} Время: {date}\n'''
EVENT_NO_EVENTS_FOUND: Final = '''Не найдено событий на сервере'''

ADD_EVENT_MSG: Final = '''Событие создано!\nНазвание: {name}\nТип: {type}\nДата: {date}'''
ADD_EVENT_CANT_CREATE: Final = '''Неудалось создать событие. Проверьте данные и попробуйте снова'''

DELETE_EVENT_MSG: Final = '''Событие: {event_id} удалено.'''
DELETE_EVENT_ARGS_NULL: Final = '''Вы не указали id события которое нужно удалить'''
DELETE_EVENT_CANT_FIND: Final = '''Не удалось найти события с данным id '''

TOO_MANY_ARGS: Final = 'Слишком много аргументов, используте !help для вызова помощи'
TOO_FEW_ARGS: Final = 'Мало аргументов, используте !help для вызова помощи'