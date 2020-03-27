from discord import Embed
from discord.ext import commands

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Help(bot))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):
        helper = Embed()
        helper.color = 0xb3b3ff
        helper.title = "⚙ List of Commands ⚙"
        movie = "🎬 Movies 🎞\nGet details from IMDb\n.kmovie movie-name"
        helper.add_field(name="\u200b", value=movie, inline=False)
        urban = "🍾UrbanDictionary🍼\nGet ud definitions\n.kdefine word"
        helper.add_field(name="\u200b", value=urban, inline=False)
        asci = "🎆Ascii🎇\nMake Fancy Text\n.kascii text"
        helper.add_field(name="\u200b", value=asci, inline=False)
        trans = "🌐Translation🌐\n💻Get Language Code\n.kgc language\n🎃Translate\n.kt langcode text"
        helper.add_field(name="\u200b", value=trans, inline=False)
        wiki = "📃Wikipedia📕\nGet Wikipedia page\n.kpage query"
        helper.add_field(name="\u200b", value=wiki, inline=False)
        server = "🎩Server info🧢\n.ksinfo"
        helper.add_field(name="\u200b", value=server, inline=False)
        fox = "🦊Foxes\n.kkoo"
        helper.add_field(name="\u200b", value=fox, inline=False)
        ping = "📱Ping📲\n.khalo"
        helper.add_field(name="\u200b", value=ping, inline=False)
        meme = "🍭Meme😂\nMake a meme\n.kmeme top-text,bottom-text"
        helper.add_field(name="\u200b", value=meme, inline=False)
        rank = "🔝Ranking🎯\nGet ranking from Ranker\n.krank url"
        helper.add_field(name="\u200b", value=rank, inline=False)
        chat = "🗣Chat😄\n🤖Random response💠\n.k?"
        helper.add_field(name="\u200b", value=chat, inline=False)
        await ctx.send(embed=helper)


