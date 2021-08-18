#https://discordapp.com/oauth2/authorize?&client_id=170000479709822976&scope=bot

import os, re

import discord
import asyncio

from .commands import handle_command

client = discord.Client()
PATTERN = re.compile(r"/([a-z]*)\s*([^\s]*)\s*(.*)")

@client.event
@asyncio.coroutine
def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)

@client.event
@asyncio.coroutine
def on_message(message):
    text = message.content
    if text.startswith("/"):
        results = PATTERN.match(text)
        if results:
            command = results.group(1)
            action = results.group(2)
            args = results.group(3)
            result = handle_command(command, action, args, message)
            if result:
                yield from client.send_message(message.channel, result)

@client.event
@asyncio.coroutine
def on_message_edit(before, after):
    pass

if __name__ == "__main__":
    client.run(os.getenv("DISCORD_ACCESS_TOKEN"))
