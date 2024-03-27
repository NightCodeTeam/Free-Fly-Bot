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

    # async def on_message(self, message):
    #    if message.author != self.user:
    #        print(
    #            f"---\n{message.guild}\n{message.channel}\n{message.author.nick}: {message.content}"
    #        )


bot = Bot()


@bot.command(name="helpme")
async def helpme(ctx: commands.Context):
    await ctx.reply("Нет :(")
