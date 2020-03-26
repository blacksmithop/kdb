import wikipedia
from discord import Embed
from discord.ext import commands

'''
def searchperson(person):
    return wikipedia.search(person, results=2)


def suggestperoson(person):
    return wikipedia.suggest(person)


def getsummary(title):
    emb = Embed()
    emb.title = title
    try:
        emb.description = wikipedia.summary(title=title)
    except wikipedia.exceptions.DisambiguationError as e:
        emb.description = e.options
    except wikipedia.exceptions.PageError:
        emb.description = f"{title} does not match any pages. Try another query!"
    return emb

'''
def getpage(page):
    emb = Embed()
    p = wikipedia.page(page)
    emb.title = p.title
    emb.url = p.url
    #emb.description = p.content[0:100]
    emb.set_image(url=p.images[0])
    return emb


class wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='page', aliases=['p'])
    @commands.guild_only()
    async def gp(self, ctx, *, args):
        await ctx.send(embed=getpage(args))


def setup(bot):
    bot.add_cog(wiki(bot))
