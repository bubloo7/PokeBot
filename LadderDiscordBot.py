"""
I run this file overnight so the bot continues to fight until I turn it off in the morning. I wanted to know the highest
rating the bot got over night so I used a discord bot to send me a message whenever a new record was reached. It was
made specifically for generation 8 random battles but should work for all formats. This file requires you to have
downloaded PokeBot and installed discord.py and poke_env.
"""

import discord
from discord.ext import commands
from PokeBot import PokeBot
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ShowdownServerConfiguration
import asyncio

# Setting up the discord bot
intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix=';', intents=intents)

# Add the token of your discord bot here
discordToken =''

# Add the id of the discord channel you want the bot to send a message to
discordChannel = 0

# Add the account details of your showdown account here
showdownUsername = ''
showdownPassword = ''


@client.event
async def on_ready():
    # Feel free to change this value
    maxRating = 1000

    player = PokeBot(
        player_configuration=PlayerConfiguration(showdownUsername, showdownPassword),
        server_configuration=ShowdownServerConfiguration, start_timer_on_battle_start=True
    )

    while True:
        await player.ladder(1)
        # I use asyncio.sleep to avoid getting marked for spam

        await asyncio.sleep(30)

        # sends message to discord channel if the bot reaches a new record
        for b in player.battles:
            print(player.battles[b])
            print(player.battles[b].rating)
            if player.battles[b].rating != None and player.battles[b].rating>maxRating:
                channel = client.get_channel(discordChannel)
                await channel.send("new record reached: " + str(player.battles[b].rating))
                maxRating = player.battles[b].rating


client.run(discordToken)