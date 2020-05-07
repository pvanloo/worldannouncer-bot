#!/usr/bin/env python3

import os
import discord
from discord.ext import commands

dragon_loc = {
    "duskwood": "The Twilight Grove, Duskwood",
    "hinterlands": "Seradane, The Hinterlands",
    "feralas": "Dream Bough, Feralas",
    "ashenvale": "Bough Shadow, Ashenvale"
}

bosses = {
    "kazzak": {
        "name": "Doom Lord Kazzak",
        "locations": {
            "blastedlands": "Blasted Lands"
        },
    },
    "emeriss": {
        "name": "Emeriss",
        "locations": dragon_loc
    },
    "lethon": {
        "name": "Lethon",
        "locations": dragon_loc        
    },
    "ysondre": {
        "name": "Ysondre",
        "locations": dragon_loc
    },
    "taerar": {
        "name": "Taerar",
        "locations": dragon_loc
    },
    "azuregos": {
        "name": "Azuregos",
        "locations": {
            "azshara": "Azshara"
        }
    }
}

if "BOT_TOKEN" not in os.environ:
    print("No token present!")
    exit(1)

if "BOT_CHANNEL_ID" not in os.environ:
    print("No channel ID present!")
    exit(1)

token = os.environ["BOT_TOKEN"]
channel_id = int(os.environ["BOT_CHANNEL_ID"])
channel = None

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="World of Warcraft Classic"))
    global channel
    channel = bot.get_channel(channel_id)
    print("Bot is ready!")

@bot.command()
async def boss(ctx, *args):

    if ctx.message.channel != channel:
        await ctx.message.add_reaction('👎')
        await ctx.message.author.send("Access the bot through the correct channel.")
        return

    # Boss supplied?
    if len(args) == 0:
        await ctx.message.add_reaction('👎')
        await ctx.send("No world boss supplied to announce!")
        ctx.command_failed = True
        return

    boss_name = args[0]

    # Boss in dict?
    if boss_name not in bosses.keys():
        await ctx.message.add_reaction('👎')
        await ctx.send(f"Did not understand world boss '{boss_name}'.")
        ctx.command_failed = True
        return

    # Location supplied
    if len(args) > 1:
        location = args[1]

        # Location is correct for boss?
        if location not in list(bosses[boss_name]["locations"].keys()):
            await ctx.message.add_reaction('👎')
            await ctx.send(f"Location '{location}' invalid for {bosses[boss_name]['name']}.") 
            ctx.command_failed = True
            return

    # No location supplied
    else:

        # Location is empty while needed?
        if (len(bosses[boss_name]["locations"]) > 1):
            await ctx.message.add_reaction('👎')
            await ctx.send(f"Need location for {bosses[boss_name]['name']}.")
            ctx.command_failed = True
            return

        location = list(bosses[boss_name]["locations"].keys())[0]            

    await ctx.message.add_reaction('👍')

    # Make announcement
    announcement = f"{bosses[boss_name]['name']} spawned! Head to {bosses[boss_name]['locations'][location]} if you can."  
  
    # Announce to members of the channel
    for member in channel.members:
        if not member.bot:
            await member.send(f"Hi {member.mention}, {announcement}")

print("Starting")
bot.run(token)