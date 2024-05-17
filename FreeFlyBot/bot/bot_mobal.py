import discord
from typing import Any
from datetime import date, datetime, timedelta
from core import create_log
from sql import EventType, Event

from settings import (
    DISCORD_MSH_TIMEOUT,
    ADD_EVENT_MODAL_NAME,
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

    ON_JOIN_MODAL_NAME,
    ON_JOIN_NAME,
    ON_JOIN_COMMENT,
    ON_JOIN_ALL_GOOD,
)


class AddEventMobal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(
            title=ADD_EVENT_MODAL_NAME,
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
            placeholder= date.today().strftime('%Y.%m.%d'), #ADD_EVENT_DATE_PLACEHOLDER,
            max_length=EVENT_DATE_MAX_CHAR,
            #row=1
        )

        # Время
        self.time_inp = discord.ui.TextInput(
            label=ADD_EVENT_TIME_NAME,
            placeholder= f'{(datetime.now() + timedelta(minutes=5) - timedelta(hours=3)).strftime('%H:%M')} (время по ET)',    #ADD_EVENT_TIME_PLACEHOLDER,
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


class OnJoinMobal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(
            title=ON_JOIN_MODAL_NAME,
            timeout=DISCORD_MSH_TIMEOUT,
            custom_id='onjoinmobal'
        )

        self.name = discord.ui.TextInput(
            label=ON_JOIN_NAME,
            #placeholder=ADD_EVENT_VIEW_NAME_PLACEHOLDER,
            #max_length=EVENT_NAME_MAX_CHAR,
            #row=1
            required=True
        )

        self.comment = discord.ui.TextInput(
            label=ON_JOIN_COMMENT,
            #placeholder=ADD_EVENT_VIEW_NAME_PLACEHOLDER,
            #max_length=EVENT_NAME_MAX_CHAR,
            #row=1,
            required=False
        )

        self.add_item(self.name)
        self.add_item(self.comment)

    async def callback(self, interaction: discord.MessageInteraction) -> Any:
        return interaction

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        create_log(error, 'error')
        return await super().on_error(interaction, error)
    
    async def on_timeout(self) -> None:
        create_log('Modal JOIN interaction timeout', 'info')
        return await super().on_timeout()
