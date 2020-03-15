import json
from random import choice
from discord.ext import commands
import discord
from googletrans import Translator, LANGUAGES

translator = Translator()
Lang_to_Code = {v: k for k, v in LANGUAGES.items()}


class globaltrans(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gc', pass_context=True)
    @commands.guild_only()
    async def getcode(self, ctx, language):
        if Lang_to_Code.get(language) is not None:
            await ctx.send(Lang_to_Code.get(language))
        else:
            await ctx.send(f"Sorry couldn't find langcode for {language}")

    @commands.command(name='t', pass_context=True)
    @commands.guild_only()
    async def trans(self, ctx, *, arg):
        src_code = arg.split(" ")[0]
        mal = translator.translate(arg[1:], dest=src_code)
        await ctx.send(mal.text)


def setup(bot):
    bot.add_cog(globaltrans(bot))
