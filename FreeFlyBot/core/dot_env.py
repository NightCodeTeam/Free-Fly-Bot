from os import environ
from dotenv import load_dotenv
from .exceptions import LoadTokenException
from settings import ENV_FILE


def update_env():
    load_dotenv(ENV_FILE)


def get_env(name) -> str:
    data = environ.get(name)
    if data is None:
        raise LoadTokenException(name)
    else:
        return data
