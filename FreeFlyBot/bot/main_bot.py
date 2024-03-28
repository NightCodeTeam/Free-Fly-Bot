import discord
from discord.ext import commands
from settings import BOT_PREFIX
from message_text import (
    HELP,
    HELP_TYPES,
    HELP_ADD_TYPE,
    HELP_DELETE_TYPE,
    HELP_EVENTS,
    HELP_ADD_EVENT,
    HELP_DELETE_EVENT,
    HELP_COMMAND_NOT_FOUND,
)


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=BOT_PREFIX, intents=intents)
        #self.help_command = None

    async def on_ready(self):
        print(f"Logged on as {self.user}!\n----")



bot = Bot()


@bot.command(name="helpme")
async def helpme(ctx: commands.Context, *args):
    print('help called')
    if len(args) == 0:
        await ctx.reply(HELP)
    else:
        msg = ''
        for i in args:
            match i:
                case 'events':
                    msg += HELP_EVENTS
                case 'addevent':
                    msg += HELP_ADD_EVENT
                case 'deletevent':
                    msg += HELP_DELETE_EVENT
                case 'types':
                    msg += HELP_TYPES
                case 'addtype':
                    msg += HELP_ADD_TYPE
                case 'deletetype':
                    msg += HELP_DELETE_TYPE
                case _:
                    msg += HELP_COMMAND_NOT_FOUND.format(i)
        await ctx.reply(msg)

@bot.command(name="events", brief='This is the brief description', description='This is the full description')
async def eventlist(ctx: commands.Context):
    await ctx.reply('ЫЫЫ')



@bot.command(name="addevent")
async def addevent(ctx: commands.Context, name: str, type: str, date: str, comment):
    await ctx.reply(f"Название: {name}\nТип: {type}\nData: {date}\nКоммент: {comment}\n")



@bot.command(name="updateevent")
async def updateevent(ctx: commands.Context):
    pass


@bot.command(name="deleteevent")
async def deleteevent(ctx: commands.Context):
    pass


@bot.command(name="types")
async def types(ctx: commands.Context):
    pass


@bot.command(name="addtype")
async def addtype(ctx: commands.Context):
    pass


                    
@bot.command(name="deletetype")
async def deletetype(ctx: commands.Context):
    pass


@bot.command(name="test2")
async def test2(ctx: commands.Context):
    pass


@bot.command(name="test1")
async def test(ctx: commands.Context):
    pass

