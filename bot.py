
from os import environ as e
import discord
from typing import List
from discord import Embed,Game,Status
from discord.ext import commands
from random import randrange as r
bot = commands.AutoShardedBot(command_prefix=e["PREFIX"], pm_help=None, description='Discord Bot for r/Kerala', shard_count=1)

initial_extensions: List[str] = ["cogs.webtest","cogs.help","cogs.wiki","cogs.movies", "cogs.globaltrans", "cogs.admin", "cogs.ascii","cogs.chatter", "cogs.fox", "cogs.urban", "cogs.memegen"]
    
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
    await bot.change_presence(status=Status.idle, activity=Game("with 🔥"))
    
def isOwner(id):
    return id == 199129403458977792

@bot.command()
async def ext(ctx, action, cog):
    COG = Embed()
    COG.title = "Cog Manager"
    if not isOwner(ctx.author.id):
        COG.description = "You are not the owner"
    else:
        if action == "unload":
            try:
                bot.unload_extension(f"cogs.{cog}")
                COG.description = f"Unloaded cog: {cog}"
            except:
                COG.description = f"Could not unload cog: {cog}"
        if action == "load":
            try:
                bot.load_extension(f"cogs.{cog}")
                COG.description = f"Load cog: {cog}"
            except:
               COG.description = f"Could not Load cog: {cog}"
    await ctx.send(embed=COG)
    
@bot.command()
async def lat(ctx):
    await ctx.send(f"Latency: {round(bot.latency, 3)}s")

@bot.command()
async def say(ctx, *, args):
    if ctx.author.id == 199129403458977792:
        await ctx.send(args)
        await ctx.message.delete()
        
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(618270738247581708)
    await channel.send(f" വരണം വരണം {member.mention}")

bot.run(e['DISCORD_TOKEN'])
