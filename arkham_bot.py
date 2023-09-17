import os
import discord
from discord.ext import tasks
from app import message_queue  # Importing the message queue from app.py

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

# Retrieve the environment variables:
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = 1142072323311144962

@tasks.loop(seconds=5)
async def background_task():
    while message_queue:
        data = message_queue.popleft()
        print(f"Sending to Discord: {data}")
        channel = client.get_channel(CHANNEL_ID)
        content = f"Transaction Alert: {data}"
        try:
            await channel.send(content)
        except Exception as e:
            print(f"Error sending message: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}({client.user.id})')
    background_task.start()

if __name__ == '__main__':
    client.run(BOT_TOKEN)
