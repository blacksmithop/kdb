import discord
from discord.ext import commands


from asyncio import sleep
class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='server', aliases=['sinfo'], pass_context=True)
    @commands.guild_only()
    async def serverinfo(self,ctx, *, guild_name=None):
        """Lists some info about the current or passed server."""

        # Check if we passed another guild
        guild = None
        if guild_name == None:
            guild = ctx.guild
        else:
            for g in self.bot.guilds:
                if g.name.lower() == guild_name.lower():
                    guild = g
                    break
                if str(g.id) == str(guild_name):
                    guild = g
                    break
        if guild == None:
            # We didn't find it
            await ctx.send("I couldn't find that guild...")
            return

        server_embed = discord.Embed(color=ctx.author.color)
        server_embed.title = guild.name

        online_members = 0
        bot_member = 0
        bot_online = 0
        for member in guild.members:
            if member.bot:
                bot_member += 1
                if not member.status == discord.Status.offline:
                    bot_online += 1
                continue
            if not member.status == discord.Status.offline:
                online_members += 1
        # bot_percent = "{:,g}%".format((bot_member/len(guild.members))*100)
        user_string = "{:,}/{:,} online ({:,g}%)".format(
            online_members,
            len(guild.members) - bot_member,
            round((online_members / (len(guild.members) - bot_member) * 100), 2)
        )
        b_string = "bot" if bot_member == 1 else "bots"
        user_string += "\n{:,}/{:,} {} online ({:,g}%)".format(
            bot_online,
            bot_member,
            b_string,
            round((bot_online / bot_member) * 100, 2)
        )
        # server_embed.add_field(name="Members", value="{:,}/{:,} online ({:.2f}%)\n{:,} {} ({}%)".format(online_members, len(guild.members), bot_percent), inline=True)
        server_embed.add_field(name="Members ({:,} total)".format(len(guild.members)), value=user_string, inline=True)
        server_embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        chandesc = "{:,} text, {:,} voice".format(len(guild.text_channels), len(guild.voice_channels))
        server_embed.add_field(name="Channels", value=chandesc, inline=True)
        server_embed.add_field(name="Default Role", value=guild.default_role, inline=True)
        server_embed.add_field(name="Owner", value=guild.owner.name + "#" + guild.owner.discriminator, inline=True)
        server_embed.add_field(name="AFK Channel", value=guild.afk_channel, inline=True)
        server_embed.add_field(name="Verification", value=guild.verification_level, inline=True)
        server_embed.add_field(name="Voice Region", value=guild.region, inline=True)
        server_embed.add_field(name="Considered Large", value=guild.large, inline=True)
        server_embed.add_field(name="Shard ID", value="{}/{}".format(guild.shard_id + 1, self.bot.shard_count), inline=True)
        server_embed.add_field(name="Nitro Boosts",
                               value="{} (level {})".format(guild.premium_subscription_count, guild.premium_tier))
        # Find out where in our join position this server is
        joinedList = []
        popList = []
        for g in self.bot.guilds:
            joinedList.append({'ID': g.id, 'Joined': g.me.joined_at})
            popList.append({'ID': g.id, 'Population': len(g.members)})

        # sort the guilds by join date
        joinedList = sorted(joinedList, key=lambda x: x['Joined'])
        popList = sorted(popList, key=lambda x: x['Population'], reverse=True)

        check_item = {"ID": guild.id, "Joined": guild.me.joined_at}
        total = len(joinedList)
        position = joinedList.index(check_item) + 1
        server_embed.add_field(name="Join Position", value="{:,} of {:,}".format(position, total), inline=True)

        # Get our population position
        check_item = {"ID": guild.id, "Population": len(guild.members)}
        total = len(popList)
        position = popList.index(check_item) + 1
        server_embed.add_field(name="Population Rank", value="{:,} of {:,}".format(position, total), inline=True)

        emojitext = ""
        emojicount = 0
        for emoji in guild.emojis:
            if emoji.animated:
                emojiMention = "<a:" + emoji.name + ":" + str(emoji.id) + ">"
            else:
                emojiMention = "<:" + emoji.name + ":" + str(emoji.id) + ">"
            test = emojitext + emojiMention
            if len(test) > 1024:
                # TOOO BIIIIIIIIG
                emojicount += 1
                if emojicount == 1:
                    ename = "Emojis ({:,} total)".format(len(guild.emojis))
                else:
                    ename = "Emojis (Continued)"
                server_embed.add_field(name=ename, value=emojitext, inline=True)
                emojitext = emojiMention
            else:
                emojitext = emojitext + emojiMention

        if len(emojitext):
            if emojicount == 0:
                emojiname = "Emojis ({} total)".format(len(guild.emojis))
            else:
                emojiname = "Emojis (Continued)"
            server_embed.add_field(name=emojiname, value=emojitext, inline=True)

        if len(guild.icon_url):
            server_embed.set_thumbnail(url=guild.icon_url)
        else:
            # No Icon
            server_embed.set_thumbnail(url=ctx.author.default_avatar_url)
        server_embed.set_footer(text="Server ID: {}".format(guild.id))
        await ctx.channel.send(embed=server_embed)
 

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
