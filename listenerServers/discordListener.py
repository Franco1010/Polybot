import discord
import aiohttp
import urllib.parse
import os
from dotenv import load_dotenv
import json

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
POLYBOT_ENDPOINT = os.getenv("POLYBOT_ENDPOINT")
intents = discord.Intents.default()
intents.messages = True


client = discord.Client(intents=intents)


async def send_message(message):
    payload = {
        "command": message.content[1:],
        "callerCtx": {
            "space": {
                "id": str(message.guild.id),
                "app": "discord",
                "name": message.guild.name,
            },
            "channel": {"id": str(message.channel.id), "name": message.channel.name},
            "author": {"id": str(message.author.id), "name": message.author.name},
        },
    }
    url = POLYBOT_ENDPOINT
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            response_json = await response.json()
            channel = message.channel
            print(response_json)
            await channel.send(
                "----------------CRYSTAALROO ---------------- \n"
                + response_json["response"]
            )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!"):
        await send_message(message)


client.run(BOT_TOKEN)
