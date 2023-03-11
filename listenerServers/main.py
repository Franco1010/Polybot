import discord
import aiohttp
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
POLYBOT_ENDPOINT = os.getenv('POLYBOT_ENDPOINT')
intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

async def send_message(message):
    query_params = {'command': message.content}
    query_string = urllib.parse.urlencode(query_params)
    url = POLYBOT_ENDPOINT + '?' + query_string
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            channel = message.channel
            await channel.send(response_json)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        await send_message(message)

client.run(BOT_TOKEN)
