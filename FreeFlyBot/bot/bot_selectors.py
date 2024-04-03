from typing import Any
from sql import EventType
import discord

from settings import (
    EVENT_TYPE_SELECTOR_PLACEHOLDER,
)


class EventTypeSelector(discord.ui.Select):
    def __init__(self, types: list[EventType]):
        self.type_name = ''
        options = []
        for ind, t in enumerate(types):
            options.append(
                discord.SelectOption(
                    label=t.type_name,
                    value=str(ind),
                    description=f'роль - {t.role_id} канал - {t.channel_id}'
                )
            )
        #options = list(
        #    map(
        #        lambda x: discord.SelectOption(
        #            label=x.type_name,
        #            value=str(x.type_id),
        #            description=f'роль - {x.role_id} канал - {x.channel_id}'
        #        ),
        #        types
        #    )
        #)

        super().__init__(
            custom_id='eventtypeselector',
            placeholder=EVENT_TYPE_SELECTOR_PLACEHOLDER,
            min_values=0,
            max_values=1,
            options=options,
            #disabled=disabled,
            #row=row
        )
    
    async def callback(self, interaction: discord.MessageInteraction) -> Any:
        return interaction

