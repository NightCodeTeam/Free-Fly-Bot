from .debug import create_log, init_logger, time_decor, call_decor
from .dot_env import get_env, update_env
from .exceptions import LoadTokenException


init_logger()
update_env()