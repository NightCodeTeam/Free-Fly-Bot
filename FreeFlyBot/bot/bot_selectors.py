from typing import Any
from sql import EventType
import discord

from settings import (
    EVENT_TYPE_SELECTOR_PLACEHOLDER,
)


class EventTypeSelector(discord.ui.Select):
    def __init__(self, types: list[EventType]):
        options = [discord.SelectOption(label=str(x), value=str(x)) for x in range(0,25)] 

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
        )
    
    async def callback(self, interaction: discord.MessageInteraction) -> Any:
        print('YES!!!!')
        print(interaction.type.value)
