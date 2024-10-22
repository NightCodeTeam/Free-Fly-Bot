from dataclasses import is_dataclass, fields
from core.debug import create_log
from .exceptions import SQLInjectionException
from settings import SQL_EXCEPT_CHARS, SQL_EXCEPT_VALUES


def parse_arg(word: str):
    # ! Слово не в запрещенных
    if word in SQL_EXCEPT_VALUES:
        create_log(f'Unsecured sql request: -> {word}')
        raise SQLInjectionException('', word)

    # ! Берем слово и проверяем что в нем нет в опасных букв
    for char in word:
        if char in SQL_EXCEPT_CHARS:
            create_log(f'Unsecured sql request: {char} -> {word}')
            raise SQLInjectionException(char, word)


def sql_protected_async(func):
    async def wrapped(*args, **kwargs):
        for arg in args:
            if type(arg) is str:
                parse_arg(arg)
            elif is_dataclass(arg):
                for field in fields(arg):
                    if field.type == str:
                        parse_arg(getattr(arg, field.name))

        return await func(*args, **kwargs)
    return wrapped


def sql_protected(func):
    """Принимаем синхронную функцию, проверяем чтобы не было опасных вставок"""
    def wrapped(*args, **kwargs):
        for arg in args:
            if type(arg) is str:
                parse_arg(arg)
            elif is_dataclass(arg):
                for field in fields(arg):
                    if field.type == str:
                        parse_arg(getattr(arg, field.name))

        return func(*args, **kwargs)
    return wrapped