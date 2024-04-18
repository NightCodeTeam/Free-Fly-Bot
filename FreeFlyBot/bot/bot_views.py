import discord
from datetime import datetime
from .bot_selectors import EventTypeSelector
from .bot_mobal import AddEventMobal, OnJoinMobal
from sql import EventType, Event, OnJoinAction, db_create_event_id
from core import make_datetime

from settings import (
    ACTIONS_COLORS,
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

    ON_JOIN_ALL_GOOD,
)


class AddEventView(discord.ui.View):
    def __init__(self, guild, types: list[EventType], author):
        super().__init__(timeout=DISCORD_MSH_TIMEOUT)
        self.author = author
        self.modal_ui = AddEventMobal()
        self.modal_ui.on_submit = self.event_conferm
        self.modal_ui.on_error = self.event_error
        self.modal_ui.on_timeout = self.event_error
        self.types = types
        self.type_index = 0

        self.event: Event | None = None

        # Тип
        self.event_type_sel = EventTypeSelector(guild, types)

        self.add_item(self.event_type_sel)
        self.event_type_sel.callback = self.prefer_event_type
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author

    async def prefer_event_type(self, interaction):
        self.type_index = self.types[int(self.event_type_sel.values[0])].type_id
        await interaction.response.send_modal(self.modal_ui)
        self.clear_items()
        self.stop()

    async def event_error(self):
        self.event = None

    async def event_conferm(self, interaction: discord.Interaction):
        date1, date2 = make_datetime(self.modal_ui.date_inp.value, self.modal_ui.time_inp.value)
        if (datetime.now() - date1).total_seconds() > 0:
            self.modal_ui.stop()
        if (datetime.now() - date2).total_seconds() > 0:
            self.modal_ui.stop()

        try:
            self.event = Event(
                await db_create_event_id(),
                interaction.message.guild.id,
                self.modal_ui.name_inp.value,
                self.type_index,
                self.modal_ui.comment_inp.value,
                date1,
                date2
            )
        except Exception:
            self.event = None

        await interaction.response.defer()

        self.modal_ui.stop()
        #self.modal_ui.clear_items()


class OnJoinButton(discord.ui.Button):
    def __init__(self, button_name: str, button_color: str, action):
        super().__init__(
            label=button_name,
            style=self.get_style(button_color)
        )
        self.pressed = False
        self.action = action

    async def callback(self, interaction):
        self.pressed = True
        await self.call(interaction)
        return interaction
    
    async def call(self, interaction):
        pass

    @staticmethod
    def get_style(color: str):
        match color:
            case 'blue':
                return discord.ButtonStyle.blurple
            case 'green':
                return discord.ButtonStyle.green
            case 'red':
                return discord.ButtonStyle.red
            case _:
                return discord.ButtonStyle.danger


class OnJoinView(discord.ui.View):
    def __init__(self, actions: list[OnJoinAction], member: discord.member.Member):
        super().__init__(timeout=DISCORD_MSH_TIMEOUT)
        self.author = member
        self.modal = OnJoinMobal()
        self.modal.on_submit = self.conferm
        self.buttons = []
        self.user_name = ''
        self.user_comment = ''
        self.action = None

        for i in actions:
            button = OnJoinButton(
                i.button_name,
                i.button_color,
                i
            )
            button.call = self.on_click
            self.buttons.append(button)
            self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author

    async def on_click(self, interaction: discord.Interaction):
        for i in self.buttons:
            if i.pressed:
                self.action = i.action
        await interaction.response.send_modal(self.modal)
        self.clear_items()
        self.stop()

    async def conferm(self, interaction: discord.Interaction):
        self.user_name = self.modal.name.value
        self.user_comment = self.modal.comment.value

        await interaction.response.send_message(ON_JOIN_ALL_GOOD)

        self.modal.clear_items()
        self.modal.stop()


class OnJoinAdminMsg(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=DISCORD_MSH_TIMEOUT)
        self.give = False

        self.confirm = discord.ui.Button(
            label='Дать роль',
            style=discord.ButtonStyle.green
        )
        self.confirm.callback = self.confirm_action

        self.cancel = discord.ui.Button(
            label='Отмена',
            style=discord.ButtonStyle.red
        )
        self.cancel.callback = self.cancel_action

        self.add_item(self.confirm)
        self.add_item(self.cancel)

    async def confirm_action(self, interaction):
        self.give = True
        await interaction.response.defer()
        self.clear_items()
        self.stop()
    
    async def cancel_action(self, interaction):
        await interaction.response.defer()
        self.clear_items()
        self.stop()
