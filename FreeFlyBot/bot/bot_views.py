import discord

from .bot_selectors import EventTypeSelector
from .bot_mobal import AddEventMobal
from sql import EventType, Event

from settings import (
    DISCORD_MSH_TIMEOUT,
    DISCORD_MSH_TIMEOUT,
    ADD_EVENT_VIEW_NAME,
    ADD_EVENT_VIEW_NAME_PLACEHOLDER,
    EVENT_TYPE_SELECTOR_PLACEHOLDER,
    ADD_EVENT_DATE_NAME,
    ADD_EVENT_DATE_PLACEHOLDER,
    ADD_EVENT_TIME_NAME,
    ADD_EVENT_TIME_PLACEHOLDER,
    ADD_EVENT_ONE_PING_BEFORE_NAME,
    ADD_EVENT_ONE_PING_BEFORE_PLACEHOLDER,
    ADD_EVENT_COMMENT_NAME,
    ADD_EVENT_COMMENT_PLACEHOLDER,
    CONFIRM_BUTTON,
    CANCEL_BUTTON,
)


class AddEventView(discord.ui.View):
    def __init__(self, types: list[EventType], author):
        super().__init__(timeout=DISCORD_MSH_TIMEOUT)
        self.author = author
        self.modal_ui = AddEventMobal()
        self.modal_ui.on_submit = self.event_conferm
        self.type_index = 0

        self.event_name = ''
        self.event_date = ''
        self.event_time = ''
        self.event_comment = ''

        # Тип
        self.event_type_sel = EventTypeSelector(types)
        

        self.add_item(self.event_type_sel)
        self.event_type_sel.callback = self.prefer_event_type
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author

    async def prefer_event_type(self, interaction):
        self.type_index = int(self.event_type_sel.values[0])
        await interaction.response.send_modal(self.modal_ui)
        self.stop()
    
    async def event_conferm(self, interaction):
        self.event_name = self.modal_ui.name_inp.value
        self.event_date = self.modal_ui.date_inp.value
        self.event_time = self.modal_ui.time_inp.value
        self.event_comment = self.modal_ui.comment_inp.value

        await interaction.response.send_message(
            f"Индекс события: {self.type_index}\nНазвание: {self.event_name}\nДата и время: {self.event_date} {self.event_time}\nКомментарий: {self.event_comment}"
        )
        
        self.modal_ui.stop()
        self.modal_ui.clear_items()
