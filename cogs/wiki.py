import wikipedia
from discord import Embed
from discord.ext import commands

def getpage(page):
    emb = Embed()
    p = wikipedia.page(page)
    emb.title = p.title
    emb.url = p.url
    emb.set_image(url=p.images[0])
    return emb

class wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='page', aliases=['wikipage'])
    @commands.guild_only()
    async def gp(self, ctx, *, args):
        await ctx.send(embed=getpage(args))

def setup(bot):
    bot.add_cog(wiki(bot))
