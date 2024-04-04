import discord
from typing import Any
from discord.utils import MISSING

from core import create_log
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

    EVENT_NAME_MAX_CHAR,
    EVENT_DATE_MAX_CHAR,
    EVENT_TIME_MAX_CHAR,
    EVENT_COMMENT_MAX_CHAR,
)


class AddEventMobal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(
            title='Создание события!',
            timeout=DISCORD_MSH_TIMEOUT,
            custom_id='addeventmobal'
        )

        # Название
        self.name_inp = discord.ui.TextInput(
            label=ADD_EVENT_VIEW_NAME,
            placeholder=ADD_EVENT_VIEW_NAME_PLACEHOLDER,
            max_length=EVENT_NAME_MAX_CHAR,
            #row=1
        )

        # Дата
        self.date_inp = discord.ui.TextInput(
            label=ADD_EVENT_DATE_NAME,
            placeholder=ADD_EVENT_DATE_PLACEHOLDER,
            max_length=EVENT_DATE_MAX_CHAR,
            #row=1
        )

        # Время
        self.time_inp = discord.ui.TextInput(
            label=ADD_EVENT_TIME_NAME,
            placeholder=ADD_EVENT_TIME_PLACEHOLDER,
            max_length=EVENT_TIME_MAX_CHAR,
            #row=1
        )

        # За 1 пинг до
        self.one_ping_b_inp = discord.ui.TextInput(
            label=ADD_EVENT_ONE_PING_BEFORE_NAME,
            placeholder=ADD_EVENT_ONE_PING_BEFORE_PLACEHOLDER,
            #row=1
        )

        # Коммент
        self.comment_inp = discord.ui.TextInput(
            label=ADD_EVENT_COMMENT_NAME,
            placeholder=ADD_EVENT_COMMENT_PLACEHOLDER,
            max_length=EVENT_COMMENT_MAX_CHAR,
            required=False
            #row=1
        )

        # Подтвердить
        #self.confirm_b = discord.ui.Button(
        #    label=CONFIRM_BUTTON,
        #    style=discord.ButtonStyle.green,
        #    row=1
        #)
        #self.confirm_b.callback = self.create_event

        # Отмена
        #self.cancel_b = discord.ui.Button(
        #    label=CANCEL_BUTTON,
        #    style=discord.ButtonStyle.red,
        #    row=5
        #)

        self.add_item(self.name_inp)
        self.add_item(self.date_inp)
        self.add_item(self.time_inp)
        #self.add_item(self.one_ping_b_inp)
        self.add_item(self.comment_inp)
        #self.add_item(self.confirm_b)
        #self.add_item(self.cancel_b)

    async def callback(self, interaction: discord.MessageInteraction) -> Any:
        return interaction

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        create_log(error, 'error')
        return await super().on_error(interaction, error)
    
    async def on_timeout(self) -> None:
        create_log('Modal interaction timeout', 'info')
        return await super().on_timeout()
