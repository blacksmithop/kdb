from subprocess import check_output

def pinghost(host):
    p = check_output(["ping", "-c", "1", host])
    p=p.decode('utf-8').split('\n')
    res = []
    for i in [0,1,4]:
        res.append(p[i])
    return res

from discord.ext import commands
from discord import Embed

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', aliases=['p'])
    @commands.guild_only()
    async def get_ping(self, ctx, host):
        member = ctx.author
        resp = Embed(title=f"pinging {host}", color=0xcc99ff)
        resp.set_author(name = member.display_name,icon_url=member.avatar_url)
        res = pinghost(host)
        resp.add_field(name="\u200b", value=res[0], inline=False)
        resp.add_field(name="\u200b", value=res[1], inline=False)
        resp.add_field(name="\u200b", value=res[2], inline=False)
        await ctx.send(embed=resp)

def setup(bot):
    bot.add_cog(ping(bot))
