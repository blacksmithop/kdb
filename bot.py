
from os import environ

from typing import List

from discord.ext import commands

bot = commands.AutoShardedBot(command_prefix='.k', pm_help=None, description='bot', shard_count=4)

initial_extensions: List[str] = ["cogs.movies", "cogs.globaltrans","cogs.OKP","cogs.admin", "cogs.ascii", "cogs.chatter", "cogs.fox", "cogs.ranker", "cogs.urban", "cogs.memegen"]

def initlialize():
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f"Cannot load {extension}")
            
initlialize()


@bot.command()
async def halo(ctx):
    await ctx.send(f"Kelkkan {round(bot.latency, 3)}sec  samayam eduthu")


@bot.command()
async def say(ctx, *, args):
    if ctx.author.id == 199129403458977792:
        await ctx.send(args)
        await ctx.message.delete()


@bot.event
async def on_ready():
    print(f"Bot id:{bot.user.id}")
    print(f"Shard count: {bot.shard_count}")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(620985606042026005)
    await channel.send(f"💪😎 {member.name} has joined, Welcome!")


@bot.event
async def on_member_leave(member):
    channel = bot.get_channel(620985606042026005)
    await channel.send(f"{member.name} has left, sed aayi")

bot.run(environ['DISCORD_TOKEN'])
