from random import randrange
from discord.ext import commands
from discord import Embed, Member
from requests import get
import ast


class floof(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fox')
    @commands.guild_only()
    async def fox(self, ctx, *, member: Member = None):
        if not member:
            member = ctx.author
        fox = Embed(title=f"🦊 {member.display_name} 🦊", color=member.color)
        fox.set_image(url=f"http://randomfox.ca/images/{randrange(1, 122)}.jpg")
        await ctx.send(embed=fox)

    @commands.command(name='cat')
    @commands.guild_only()
    async def cat(self, ctx, *, member: Member = None):
        if not member:
            member = ctx.author
        nya = Embed(title=f"😸 {member.display_name} 🐱‍", color=member.color)
        kitto = ast.literal_eval(get('https://aws.random.cat/meow').content.decode('utf-8'))
        url = kitto['file'].replace('\\', '')
        nya.set_image(url=url)
        await ctx.send(embed=nya)

    @commands.command(name='dog')
    @commands.guild_only()
    async def dog(self, ctx, *, member: Member = None):
        if not member:
            member = ctx.author
        woof = Embed(title=f"😸 {member.display_name} 🐱‍", color=member.color)
        doggo = ast.literal_eval(get('https://random.dog/woof.json').content.decode('utf-8'))
        url = doggo['url'].replace('\\', '')
        woof.set_image(url=url)
        await ctx.send(embed=woof)


def setup(bot):
    bot.add_cog(floof(bot))
