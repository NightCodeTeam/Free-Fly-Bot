from sys import argv
from core import create_log, get_env, update_env
from bot import bot

# intents = discord.Intents.default()
# intents.message_content = True


# class MyClient(discord.Client):
#    async def on_ready(self):
#        print(f"Logged on as {self.user}!")
#        for guild in list(self.guilds):
#            for channel in guild.channels:
#                print(channel.name)
#
#                a = discord.Bot
#
#    async def on_message(self, message):
#        # pprint(f'{message}')
#        print(
#            f"{message.guild}\n{message.channel}\nMessage from {message.author.nick}: {message.content}"
#        )
#


def main(args):
    update_env()
    bot.run(get_env("BOT_TOKEN"))


if __name__ == "__main__":
    try:
        main(argv[1:])
    except Exception as err:
        create_log(err, "crit")
