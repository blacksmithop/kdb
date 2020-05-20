
from os import environ as e
import discord
from typing import List
from discord import Embed,Game,Status,Colour,Member
from discord.ext import commands
from random import randrange as r
from asyncio import TimeoutError
bot = commands.AutoShardedBot(command_prefix=e["PREFIX"], pm_help=None, description='Discord Bot for r/Kerala', shard_count=4)

initial_extensions: List[str] = ["cogs.economy","cogs.webtest","cogs.wiki","cogs.movies", "cogs.globaltrans", "cogs.admin", "cogs.ascii","cogs.chatter", "cogs.fox", "cogs.urban", "cogs.memegen"]

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

from ast import literal_eval as l
from requests import get
from random import shuffle as s

   
bot.remove_command("help")
@bot.command()
async def help(ctx):
    cmd = [
        "🎩Server info🧢\n.ksinfo",
        "📱Latency📲\n.klat",
        "🦹‍♂️View Avatar Image\n.kview user",
        "🎆Ascii🎇\nMake Fancy Text\n.kascii text",
        "🗣ChatBot😄\n🤖.k? (malayalam)💠\n.k?? (english)",
        "Random🦊Foxes\n.kfox",
        "Random😸Cats\n.kcat",
        "Random🐶Dogs\n.kdog",
        "🌐Translation🌐\n💻Get Language Code\n.kgc language\n\n🎃Translate\n.kt langcode text",
        "🍭Meme😂\nMake a meme\n.kmeme top-text,bottom-text",
        "🎬 Movies 🎞\nGet details from IMDb\n.kmovie",
        "🍾UrbanDictionary🍼\nGet UD definitions\n.kdefine word",
        "📱Ping📲\n.kping url",
        "📃Wikipedia📕\nGet Wikipedia page\n.kpage query",
        "❓Trivia\n.ktrivia ✅"
        ]

    p = [[0,4],[5,9],[10,14]]
    def createpage(i):
        des = ""
        for i in range(p[i][0],p[i][1]+1):
            des+=f"```{cmd[i]}```\n"
        return des

    react = ["◀","▶","🛑"]
    msg = await ctx.send(embed=Embed(
            title=f'Help ({1})',
            description=createpage(0),
            colour=Colour.orange()))
    for emoji in react:
        await msg.add_reaction(emoji)
    page = 0
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=20.0)
            em = str(reaction.emoji)
        except TimeoutError:
            await msg.edit(content="```Command timed out ⌚!```")
        if em == react[1]:
            await msg.remove_reaction(emoji=em,member=user)
            if page==2:
                pass
            else:
                page+=1
                await msg.edit(embed=Embed(
                    title=f'Help ({page+1})',
                    description=createpage(page),
                    colour=Colour.orange()))
        if em == react[0]:
            await msg.remove_reaction(emoji=em,member=user)
            if page==0:
                pass
            else:
                page-=1
                await msg.edit(embed=Embed(
                    title=f'Help ({page+1})',
                    description=createpage(page),
                    colour=Colour.orange()))
        if em == react[2] and user!=bot.user:
            await msg.clear_reactions()
            await msg.edit(embed=Embed(
                title='Bye!',
                description="```👋```",
                colour=Colour.orange()))
            break
            
@bot.command()
async def lat(ctx):
    await ctx.send(f"Latency: {round(bot.latency, 3)}s")

@bot.command()
async def say(ctx, *, args):
    if ctx.author.id == 199129403458977792:
        await ctx.send(args)
        await ctx.message.delete()


bot.run(e['DISCORD_TOKEN'])
