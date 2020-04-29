from discord.ext import commands
from googletrans import Translator, LANGUAGES

translator = Translator()
Lang_to_Code = {v: k for k, v in LANGUAGES.items()}


class globaltrans(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gc')
    @commands.guild_only()
    async def getcode(self, ctx, language):
        if Lang_to_Code.get(language.lower()) is not None:
            await ctx.send(Lang_to_Code.get(language.lower()))
        else:
            await ctx.send(f"Sorry couldn't find langcode for {language}")

    @commands.command(name='t')
    @commands.guild_only()
    async def trans(self, ctx, *, arg):
        mal = translator.translate(arg.split(' ', 1)[1], dest=arg.split(' ', 1)[0])
        await ctx.send(mal.text)


def setup(bot):
    bot.add_cog(globaltrans(bot))
