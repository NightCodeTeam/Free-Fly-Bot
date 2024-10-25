from .debug import create_log, init_loggers, call_log, LoggerConfig, RotatingHandlerConfig
from .dot_env import get_env, update_env
from .exceptions import LoadTokenException


init_loggers(
    LoggerConfig(
        'logger.log',
        'debug',
        (
            RotatingHandlerConfig(
                maxBytes=1_000,
                backupCount=1
            ),
        )
    ),
    LoggerConfig(
        'error.log',
        'error'
    )
)
update_env()