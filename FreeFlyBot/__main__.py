from pprint import pprint
import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        #pprint(f'{message}')
        print(f'{message.guild}\n{message.channel}\nMessage from {message.author.nick}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run('token')