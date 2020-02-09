from discord.ext import commands
from os import environ
from discord import Embed, Color
bot = commands.AutoShardedBot(command_prefix='?', pm_help=None, description='bot', shard_count=4)

initial_extensions = ["cogs.admin","cogs.fox"]
#all the init stuff goes here until I figure out Sharding better
def initlialize():
    for extension in initial_extensions:
        bot.load_extension(extension)

initlialize()

@bot.command()
async def halo(ctx):
    await ctx.send(f"Kelkkan {round(bot.latency,3)}sec  samayam eduthu")


@bot.event
async def on_ready():
    print(f"Bot id:{bot.user.id}")
    print(f"Shard count: {bot.shard_count}")

@bot.event
async def on_member_join(member):
    # replace channel ID with welcoming channel (bot has write perms)
    channel = bot.get_channel(561109092639309828)
    await channel.send(f"💪😎 {member.name} has joined")

@bot.command(pass_context=True)
async def listroles(ctx):
    for role in ctx.guild.roles:
        roles = Embed(title="Roles",color=0xefefef)
        roles.add_field(name="\u200b",value=role)
    await ctx.send(embed=roles)
#Will work once we keep a db of users, needs work
'''
@bot.event
async def on_member_leave(member):
    channel = bot.get_channel(561109092639309828)
    await channel.send(f"{member.name} has left, sed aayi")
    '''

bot.run(environ['DISCORD_TOKEN'])
