import os
from flask import Flask, request, jsonify, abort
import discord
from discord.ext import tasks
import asyncio
from collections import deque
import threading

app = Flask(__name__)

# Define the necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# Initialize the Discord client with the required intents
client = discord.Client(intents=intents)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = 1142072323311144962

# Create a queue to hold messages that we want to send to Discord
message_queue = deque()

@tasks.loop(seconds=5)
async def background_task():
    while message_queue:
        data = message_queue.popleft()
        print(f"Sending to Discord: {data}")  # Debug print
        channel = client.get_channel(CHANNEL_ID)
        content = f"Transaction Alert: {data}"
        try:
            await channel.send(content)
        except Exception as e:
            print(f"Error sending message: {e}")

@app.route('/webhook', methods=['POST'])
def webhook_listener():
    webhook_token = request.headers.get('Arkham-Webhook-Token')

    valid_tokens = {'Kep9w4rCgMx09o', 'Token2', 'Token3'}  # Add your valid tokens to this set
    if webhook_token not in valid_tokens:
        abort(403)  # Forbidden, incorrect token

    data = request.json
    print(data)

    # Append data to our queue
    message_queue.append(data)
    print(f"Current Queue: {message_queue}")  # Debug print

    return jsonify({"message": "Received and forwarded"}), 200

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}({client.user.id})')
    background_task.start()

def run_discord():
    asyncio.run(client.start(BOT_TOKEN))

if __name__ == '__main__':
    # Start the Discord bot in a separate thread
    threading.Thread(target=run_discord, daemon=True).start()
    # Run the Flask app in the main thread
    app.run(host='0.0.0.0')
