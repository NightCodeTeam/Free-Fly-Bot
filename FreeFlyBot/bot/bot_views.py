from typing import Any
from sql import EventType, Event
import discord


class AddEventView(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)

        