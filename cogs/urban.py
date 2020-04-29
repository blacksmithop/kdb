import asyncio
import discord
import string
import random
from urllib.parse import quote
from discord.ext import commands
from cogs.Addons import Message
from cogs.Addons import DL

def setup(bot):
    bot.add_cog(UrbanDict(bot))

class UrbanDict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.random = True
        self.ua = 'Kunjan'
    @commands.command(pass_context=True)
    async def define(self, ctx, *, word: str = None):
        if not word:
            msg = 'Usage: `{}define [word]`'.format(ctx.prefix)
            await ctx.channel.send(msg)
            return
        url = "http://api.urbandictionary.com/v0/define?term={}".format(quote(word))
        msg = 'I couldn\'t find a definition for "{}"...'.format(word)
        title = permalink = None
        theJSON = await DL.async_json(url, headers={'User-agent': self.ua})
        theJSON = theJSON["list"]
        if len(theJSON):
            if self.random:
                ourWord = random.choice(theJSON)
            else:
                ourWord = theJSON[0]
            msg = '__**{}:**__\n\n{}'.format(string.capwords(ourWord["word"]), ourWord["definition"])
            if ourWord["example"]:
                msg = '{}\n\n__**Example(s):**__\n\n*{}*'.format(msg, ourWord["example"])
            permalink = ourWord["permalink"]
            title = "Urban Dictionary Link"

        await Message.EmbedText(title=title, description=msg, color=ctx.author, url=permalink).send(ctx)

    @commands.command(pass_context=True)
    async def randefine(self, ctx):
        url = "http://api.urbandictionary.com/v0/random"
        title = permalink = None
        theJSON = await DL.async_json(url, headers={'User-agent': self.ua})
        theJSON = theJSON["list"]
        if len(theJSON):
            if self.random:
                ourWord = random.choice(theJSON)
            else:
                ourWord = theJSON[0]
            msg = '__**{}:**__\n\n{}'.format(string.capwords(ourWord["word"]), ourWord["definition"])
            if ourWord["example"]:
                msg = '{}\n\n__**Example(s):**__\n\n*{}*'.format(msg, ourWord["example"])
            permalink = ourWord["permalink"]
            title = "Urban Dictionary Link"
        await Message.EmbedText(title=title, description=msg, color=ctx.author, url=permalink).send(ctx)