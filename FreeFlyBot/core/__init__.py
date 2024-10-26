from .debug import create_log, init_loggers, call_log, LoggerConfig, RotatingHandlerConfig, StreamHandlerConfig
from .dot_env import get_env, update_env
from .exceptions import LoadTokenException


init_loggers(
    LoggerConfig(
        'logger',
        'debug',
        (
            RotatingHandlerConfig(
                maxBytes=1_000,
                backupCount=1
            ),
            StreamHandlerConfig()
        )
    ),
    LoggerConfig(
        'error',
        'error'
    )
)
update_env()