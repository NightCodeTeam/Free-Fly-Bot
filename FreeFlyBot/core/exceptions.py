from .debug import create_log


class LoadTokenException(Exception):
    def __init__(self, error: Exception | str):
        self.txt = f'Cant load token: {error}'
        create_log(self.txt)
        super().__init__(self.txt)
