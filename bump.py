from discord.ext import commands
from discord import Embed
from time import sleep
from os import environ
bot = commands.Bot(command_prefix='..', description='''Bump''', self_bot=True)

@bot.event
async def on_ready():
    print("running")

@bot.command()
async def hi(ctx):
    BUMP = Embed()
    BUMP.title = "**Auto Bump**"
    BUMP.color = 0x9dfc03
    bump_count = 0
    while True:
        BUMP.description = f"Count: {bump_count}"
        bump_count+=1
        await ctx.send(embed=BUMP)
        sleep(1)
        await ctx.send("!d bump")
        sleep(7200)

bot.run(environ['token'],bot=False)
