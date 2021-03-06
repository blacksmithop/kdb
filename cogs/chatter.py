import json
from random import choice
from discord.ext import commands
import discord
from googletrans import Translator

translator = Translator()

with open('cogs/responses.json', 'r') as r:
    responses = json.load(r)['responses']

with open('cogs/english.json', 'r') as r:
    english = json.load(r)['responses']

class solla(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='?', pass_context=True)
    @commands.guild_only()
    async def parachil(self, ctx):
        await ctx.send(choice(responses))

    @commands.command(name='??', pass_context=True)
    @commands.guild_only()
    async def talker(self, ctx):
        await ctx.send(choice(english))

    @commands.command(name='m', pass_context=True)
    @commands.guild_only()
    async def mtrans(self, ctx, *, arg):
        mal = translator.translate(arg, dest="ml")
        await ctx.send(mal.text)

    @commands.command(name='h', pass_context=True)
    @commands.guild_only()
    async def htrans(self, ctx, *, arg):
        hin = translator.translate(arg, dest="hi")
        await ctx.send(hin.text)

def setup(bot):
    bot.add_cog(solla(bot))