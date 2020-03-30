import discord
from random import randrange
from discord.ext import commands
from requests import get
import ast

class floof(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='koo', aliases=['kurukkan'])
    @commands.guild_only()
    async def fox(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        fox = discord.Embed(title=f"🦊 {member.display_name} 🦊", color=member.color)
        fox.set_image(url=f"http://randomfox.ca/images/{randrange(1,122)}.jpg")
        await ctx.send(embed=fox)

    @commands.command(name='moew', aliases=['cat'])
    @commands.guild_only()
    async def cat(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        nya = discord.Embed(title=f"😸 {member.display_name} 🐱‍", color=member.color)
        kitto = ast.literal_eval(get('https://aws.random.cat/meow').content.decode('utf-8'))
        url = kitto['file'].replace('\\','')
        nya.set_image(url=url)
        await ctx.send(embed=nya)

    @commands.command(name='dog', aliases=['bark'])
    @commands.guild_only()
    async def bow(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        woof = discord.Embed(title=f"😸 {member.display_name} 🐱‍", color=member.color)
        doggo = ast.literal_eval(get('https://random.dog/woof.json').content.decode('utf-8'))
        url = doggo['url'].replace('\\', '')
        print(url)
        woof.set_image(url=url)
        await ctx.send(embed=woof)

def setup(bot):
    bot.add_cog(floof(bot))
