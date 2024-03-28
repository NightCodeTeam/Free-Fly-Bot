class LoadTokenException(Exception):
    def __init__(self):
        self.txt = 'Cant load token to bot'
        super().__init__(self.txt)
