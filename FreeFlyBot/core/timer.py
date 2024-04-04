from asyncio import gather, run
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
        self.near = None
        self.events = []
    
    async def time_to_nearest_event(self) -> Event | None:
        self.near = await db_get_nearest_event()
        #return await db_get_nearest_event()
    
    async def all_events(self) -> list[Event]:
        self.events = await db_get_events_list()
        #return await db_get_events_list()

    async def main(self):
        await gather(self.time_to_nearest_event(), self.all_events())
    
    def run(self):
        run(self.main())
        print(self.near)
        print(self.events)
