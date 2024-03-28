import discord
from discord.ext import commands
from settings import BOT_PREFIX


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=BOT_PREFIX, intents=intents)

    async def on_ready(self):
        print(f"Logged on as {self.user}!\n----")



bot = Bot()


@bot.command(name="helpme")
async def helpme(ctx: commands.Context):
    await ctx.reply("Нет :(")


@bot.command(name="eventlist", brief='This is the brief description', description='This is the full description')
async def eventlist(ctx: commands.Context):
    await ctx.reply('ЫЫЫ')

 

@bot.command(name="addevent")
async def addevent(ctx: commands.Context):
    pass



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

