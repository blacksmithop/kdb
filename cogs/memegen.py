import discord
from discord.ext import commands
from random import choice
import json

with open('./cogs/urlmap') as src:
    urljson = json.load(src)


# BASE_URL = 'https://memegen.link/joker/why/so_serious'
# GOT_URL = 'https://memegen.link/api/templates/morpheus'
# URL_YOU_NEED = 'https://memegen.link/tenguy/1/3.jpg'

class memegen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='meme', aliases=['makememe'])
    @commands.guild_only()
    async def getmeme(self, ctx, *, args):
        member = ctx.author
        args = args.split(',')
        randmeme = choice(list(urljson.items()))
        meme_name = randmeme[1].split("templates/", 1)[1]

        meme = discord.Embed(title=f"😜{member.display_name} 😆", color=member.color)
        memeurl = f"https://memegen.link/{meme_name}/{args[0]}/{args[1]}.jpg"

        meme.set_image(url=memeurl)
        await ctx.send(embed=meme)


def setup(bot):
    bot.add_cog(memegen(bot))
