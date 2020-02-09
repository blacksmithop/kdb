import discord
from discord.ext import commands


from asyncio import sleep
class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member = None):
        """Find Join date"""
        if member is None:
            member = ctx.author
        await ctx.send(f'{member.display_name} joined on {member.joined_at}')

    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member = None):
        """Shows the members Top Role."""

        if member is None:
            member = ctx.author

        await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')

    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member = None):
        """Checks a members Server Permissions.
        If no member provided, check the author"""

        if not member:
            member = ctx.author

        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, i.e empty field name.
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)

    @commands.command(name='info', aliases=['view'])
    @commands.guild_only()
    async def user_stats(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        embed = discord.Embed(title=f"{member.display_name}", color=member.color)
        embed.set_image(url=member.avatar_url)

        await ctx.send(content=None, embed=embed)

    @commands.command(name='promote', aliases=['addrole'],pass_context=True)
    @commands.guild_only()
    async def add_role(self, ctx, *, member: discord.Member = None):
        channel = self.bot.get_channel(561109092639309828)
        await  channel.send("Etha role?")
        #msg = await channel.history().get(author__name=member.display_name)
        rolename=""
        await sleep(3)
        async for msg in channel.history(limit=1):
            if member.display_name == msg.author.name:
                rolename = msg.content
        #await member.add_roles(rolename)
        await ctx.send(f"Added role {rolename}")

def setup(bot):
    bot.add_cog(utility(bot))
