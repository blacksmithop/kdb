
from os import environ as e
import discord
from typing import List
from discord import Embed,Game,Status,Colour,Member
from discord.ext import commands
from random import randrange as r
from asyncio import TimeoutError
bot = commands.AutoShardedBot(command_prefix=e["PREFIX"], pm_help=None, description='Discord Bot for r/Kerala', shard_count=4)

initial_extensions: List[str] = ["cogs.userdata"]

def initlialize():
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f"Cannot load {extension}")
          
@bot.event
async def on_ready():
    print(f"Bot id:{bot.user.id}")
    print(f"Shard count: {bot.shard_count}")
    initlialize()
    await bot.change_presence(status=Status.idle, activity=Game(".khelp"))
    bot.remove_command("help")


bot.run(e['DISCORD_TOKEN'])
