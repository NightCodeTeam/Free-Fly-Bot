from os import remove
from os.path import exists
from core import create_log


def delete_file(path_to_file: str) -> bool:
    if exists(path_to_file):
        remove(path_to_file)
        return True
    return False
