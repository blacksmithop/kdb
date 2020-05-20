from os import environ as e
from redis import Redis
from json import dumps, loads
from discord import Embed, Member, Status, Colour
from discord.ext import commands

event_channel = 618270738247581708

rdb = Redis(
    host=e["host"],
    port=17489,
    password=e["pwd"])


def UserSchema(member: Member, action: str = None, amt: int = None, task: str = None, nick: str = None):
    if action == "add":
        user = {
            "nick": [],
            "bal": amt,
            "daily": None
        }
        juser = dumps(user)
        rdb.set(member.id, juser)
    if action == "remove":
        rdb.delete(member.id)
    if action == "get":
        if task == "nickget":
            user = loads(rdb.get(member.id))
            return user["nick"]
        if task == "nickadd":
            user = loads(rdb.get(member.id))
            user["nick"].append(nick)
            juser = dumps(user)
            rdb.set(member.id, juser)


class userdata(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, ctx, member: Member = None):

        if member is None:
            member = ctx.author
        data = Embed()
        data.title = member.display_name
        data.add_field(name="Joined", value=member.joined_at.strftime("%m/%d/%Y"), inline=True)
        data.add_field(name="Top Role", value=member.top_role, inline=True)
        s2c = {
            Status.online: "🟢",
            Status.do_not_disturb: "🔕",
            Status.idle: "🌙",
            Status.offline: "👻"
        }
        data.add_field(name="Status", value=s2c[member.status], inline=True)
        data.add_field(name="Activity", value=member.activity, inline=True)
        m2c = {
            True: "📱",
            False: "📵"
        }
        data.add_field(name="Mobile", value=m2c[member.is_on_mobile()], inline=True)

        nick = UserSchema(member=member, action="get", task="nickget")
        if len(nick) == 0:
            nick = [member.display_name]
        data.add_field(name="Nicks", value=", ".join(nick), inline=True)
        data.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=data)

    @commands.command()
    async def migrate(self, ctx):
        for guild in self.bot.guilds:
            for member in guild.members:
                if not member.bot:
                    if rdb.get(member.id) is None:
                        print(member.display_name)
                        UserSchema(member=member, action="add", amt=10)
        await ctx.send("```Migrated to V2```")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.nick is not None and before.nick != after.nick:
            UserSchema(member=after, action="get", task="nickadd", nick=after.nick)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        greet = self.bot.get_channel(event_channel)
        await greet.send(embed=Embed(
            description=f"{member.mention} Welcome to r/Kerala 🌴 Discord!",
            color=Colour.dark_magenta()
        ).set_image(url="https://cdn.discordapp.com/icons/618270738247581706/cbf6fc13cb3c26dfcbc021e7ae272c1d.webp?size=128"))
        UserSchema(member=member, action="add", amt=10)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        UserSchema(member=member, action="remove")

    '''@commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        greet = self.bot.get_channel(event_channel)
        await greet.send(embed=Embed(
            description=f"{member.display_name}\n was Banned 🔨",

            color=Colour.dark_gold()
        ).set_image(url="https://tenor.com/view/thor-avenger-chris-hemsworth-mjolnir-gif-13624915"))
    '''

def setup(bot):
    bot.add_cog(userdata(bot))
