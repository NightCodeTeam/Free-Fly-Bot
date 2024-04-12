import logging
from logging.handlers import RotatingFileHandler
from typing import Literal
from time import time

from settings import (
    DEBUG,
    LOGGER_LEVEL,
    MAIN_LOGGER,
    MAIN_LOGGER_MAX_BITES,
    ERROR_LOGGER,
)

Level = Literal['debug', 'warning', 'info', 'error', 'crit']


def set_level(handler, levelname: Level):
    match levelname:
        case 'debug':
            handler.setLevel(logging.DEBUG)
        case 'warning':
            handler.setLevel(logging.WARNING)
        case 'info':
            handler.setLevel(logging.INFO)
        case 'error':
            handler.setLevel(logging.ERROR)
        case 'crit':
            handler.setLevel(logging.CRITICAL)


def init_logger():
    # Главный логгер
    main_logger = logging.getLogger(MAIN_LOGGER)
    set_level(main_logger, LOGGER_LEVEL)
    main_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    # Файловый логер
    main_handler_file = RotatingFileHandler(
        filename=f'{MAIN_LOGGER}.log',
        mode='a',
        maxBytes=MAIN_LOGGER_MAX_BITES,
        backupCount=1,
    )
    main_handler_file.setFormatter(main_formatter)
    main_logger.addHandler(main_handler_file)

    # Добавляем логироваеие в консоль
    if DEBUG:
        main_handler_console = logging.StreamHandler()
        main_handler_console.setFormatter(main_formatter)
        main_logger.addHandler(main_handler_console)

    # Логгер ошибок
    error_logger = logging.getLogger(ERROR_LOGGER)
    error_logger.setLevel(logging.ERROR)

    # Файловый логгер
    error_handler_file = logging.FileHandler(
        filename=f'{ERROR_LOGGER}.log',
        mode='a',
    )
    error_handler_file.setFormatter(main_formatter)
    error_logger.addHandler(error_handler_file)

    # Консольный логгер
    if not DEBUG:
        error_handler_console = logging.StreamHandler()
        error_handler_console.setFormatter(main_formatter)
        error_logger.addHandler(error_handler_console)


def call_decor(func):
    def wrapper(*args, **kwarks):
        func(*args, **kwarks)
        create_log(f'Function {func.__name__} called!', 'debug')
    return wrapper


def time_decor(func):
    def wrapper(*args, **kwarks):
        st = time()
        func(*args, **kwarks)
        create_log(f'{func.__name__} complete in {time() - st}', 'debug')
    return wrapper


def create_log(
    log: Exception | str,
    level_name: Level = 'debug',
):
    main_logger = logging.getLogger(MAIN_LOGGER)
    error_logger = logging.getLogger(ERROR_LOGGER)

    log_exc = False
    if type(log) is not str:
        log_exc = True
    match level_name:
        case 'debug':
            main_logger.debug(log, exc_info=log_exc)
        case 'warning':
            main_logger.warning(log, exc_info=log_exc)
        case 'info':
            main_logger.info(log, exc_info=log_exc)
        case 'error':
            main_logger.error(log, exc_info=log_exc)
            error_logger.error(log, exc_info=log_exc)
        case 'crit':
            main_logger.error(log, exc_info=log_exc)
            error_logger.error(log, exc_info=log_exc)
