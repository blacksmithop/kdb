import discord
from random import randrange
from discord.ext import commands


class floof(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='koo', aliases=['fox'])
    @commands.guild_only()
    async def kurkukkan(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        fox = discord.Embed(title=f"🦊 {member.display_name} 🦊", color=member.color)
        fox.set_image(url=f"http://randomfox.ca/images/{randrange(1,122)}.jpg")
        await ctx.send(embed=fox)

def setup(bot):
    bot.add_cog(floof(bot))
