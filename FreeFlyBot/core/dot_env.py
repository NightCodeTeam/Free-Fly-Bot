from os import environ, path, listdir
from dotenv import load_dotenv
from settings import ENV_FILE


def update_env():
    load_dotenv(ENV_FILE)


def get_env(name):

    return environ.get(name)
