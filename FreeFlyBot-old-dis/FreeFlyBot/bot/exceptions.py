class CallFuncBotNotInGuildException(Exception):
    def __init__(self, func):
        self.txt = f'Called func "{func}" but guild not found'
        super().__init__(self.txt)
