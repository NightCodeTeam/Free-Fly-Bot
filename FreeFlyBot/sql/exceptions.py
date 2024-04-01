class SQLCantGetIDsException(Exception):
    def __init__(self, table):
        self.txt = f'SQL CANT get ids from table {table}'
        super().__init__(self.txt)


class SQLFullException(Exception):
    def __init__(self, table):
        self.txt = f'SQL TOO MANY ENTRIES {table}'
        super().__init__(self.txt)