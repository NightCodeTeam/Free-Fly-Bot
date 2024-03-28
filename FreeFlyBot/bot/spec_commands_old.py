from discord.ext import commands


class MyHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, ctx):
        print(ctx.keys())
        #return await ctx.send('Это моя собственная команда помощи!')
