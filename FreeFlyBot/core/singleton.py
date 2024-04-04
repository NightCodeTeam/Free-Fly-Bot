
class SingletonLarger:
    """Класс создающий 1 экзепляр при любом количестве инициализаций.\
        Для работы нужно лишь указать этот класс как родителя."""
    _instances = {}
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton:
    """Создает единственный экземпляр класса в системе.
Использование: Укажите этот класс в качестве родителя."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance