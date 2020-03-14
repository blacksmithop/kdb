import asyncio
import discord
import string
import random
from urllib.parse import quote
from discord.ext import commands
from cogs.Addons import Message
from cogs.Addons import DL


def setup(bot):
    # Add the bot and deps
    bot.add_cog(UrbanDict(bot))


# This module grabs Urban Dictionary definitions

class UrbanDict(commands.Cog):

    # Init with the bot reference, and a reference to the settings var and xp var
    def __init__(self, bot):
        self.bot = bot
        self.random = True
        self.ua = 'Kunjan'
    @commands.command(pass_context=True)
    async def define(self, ctx, *, word: str = None):
        """Gives the definition of the word passed."""
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
            # Got it - let's build our response
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

    # await Message.say(self.bot, msg, ctx.message.channel, ctx.message.author)

    @commands.command(pass_context=True)
    async def randefine(self, ctx):
        """Gives a random word and its definition."""
        url = "http://api.urbandictionary.com/v0/random"
        title = permalink = None
        theJSON = await DL.async_json(url, headers={'User-agent': self.ua})
        theJSON = theJSON["list"]
        if len(theJSON):
            # Got it - let's build our response
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