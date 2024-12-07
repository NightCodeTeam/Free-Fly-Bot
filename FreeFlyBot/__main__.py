import asyncio
from sys import argv
from core.debug import create_log
from api.fastapi_main import ServerMain


def run_server():
    server = ServerMain()
    server.run()

def main(args: list):
    run_server()


if __name__ == "__main__":
    try:
        create_log(f'Run main: {argv}')
        main(argv[1:])
    except Exception as err:
        create_log(err, "crit")
