from datetime import datetime
from .singleton import Singleton
from sql import (
    Event,
    db_get_nearest_event,
    db_get_events_list
)


class Timer(Singleton):
    def __init__(self) -> None:
        super().__init__()
    
    async def time_to_nearest_event(self) -> Event | None:
        return await db_get_nearest_event()
    
    async def all_events(self) -> list[Event]:
        return await db_get_events_list()
