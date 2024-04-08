from typing import Any
from sql import EventType
import discord

from settings import (
    EVENT_TYPE_SELECTOR_PLACEHOLDER,
)


class EventTypeSelector(discord.ui.Select):
    def __init__(self, guild, types: list[EventType]):
        self.type_name = ''
        options = []

        for ind, t in enumerate(types):
            options.append(
                discord.SelectOption(
                    label=t.type_name,
                    value=str(ind),
                    description=f'Роль - {guild.get_role(t.role_id)} Канал - {guild.get_channel(t.channel_id)}'
                )
            )

        super().__init__(
            custom_id='eventtypeselector',
            placeholder=EVENT_TYPE_SELECTOR_PLACEHOLDER,
            min_values=0,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.MessageInteraction) -> Any:
        return interaction

