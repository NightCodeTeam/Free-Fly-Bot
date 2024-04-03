import discord

from .bot_selectors import EventTypeSelector
from sql import EventType, Event

from settings import (
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
    def __init__(self, types: list[EventType]):
        super().__init__(timeout=180)
        self.create = False

        # Название
        self.name_inp = discord.ui.TextInput(
            label=ADD_EVENT_VIEW_NAME,
            placeholder=ADD_EVENT_VIEW_NAME_PLACEHOLDER,
            row=0
        )

        # Тип
        self.event_type_sel = EventTypeSelector(types, 1)

        # Дата
        self.date_inp = discord.ui.TextInput(
            label=ADD_EVENT_DATE_NAME,
            placeholder=ADD_EVENT_DATE_PLACEHOLDER,
            row=2
        )

        # Время
        self.time_inp = discord.ui.TextInput(
            label=ADD_EVENT_TIME_NAME,
            placeholder=ADD_EVENT_TIME_PLACEHOLDER,
            row=2
        )

        # За 1 пинг до
        self.one_ping_b_inp = discord.ui.TextInput(
            label=ADD_EVENT_ONE_PING_BEFORE_NAME,
            placeholder=ADD_EVENT_ONE_PING_BEFORE_PLACEHOLDER,
            row=3
        )

        # Коммент
        self.comment_inp = discord.ui.TextInput(
            label=ADD_EVENT_DATE_NAME,
            placeholder=ADD_EVENT_DATE_PLACEHOLDER,
            row=4
        )

        # Подтвердить
        self.confirm_b = discord.ui.Button(
            label=CONFIRM_BUTTON,
            style=discord.ButtonStyle.green,
            row=5
        )
        self.confirm_b.callback = self.create_event

        # Отмена
        self.cancel_b = discord.ui.Button(
            label=CANCEL_BUTTON,
            style=discord.ButtonStyle.red,
            row=5
        )

        self.add_item(self.name_inp)
        self.add_item(self.event_type_sel)
        self.add_item(self.date_inp)
        self.add_item(self.time_inp)
        self.add_item(self.one_ping_b_inp)
        self.add_item(self.comment_inp)
        self.add_item(self.confirm_b)
        self.add_item(self.cancel_b)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == interaction.message.author

    def create_event(self, *args):
        self.create = True
        self.stop()