
from requests import get
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from time import sleep

class ranker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='getranked', aliases=['rank'])
    @commands.guild_only()
    async def topfive(self, ctx,url):
        member = ctx.author
        page = get(url)
        # print(page.status_code)

        soup = BeautifulSoup(page.content, 'html.parser')
        clsname='listItem__title listItem__title--link black'
        imname = 'listItem__image'
        name = soup.find_all(class_=clsname)
        image = soup.find_all(class_=imname)

        #for item in image:
            #print(item['src'])

        #for item in name:
            #print(item.encode_contents().decode("utf-8"))
        for i in range(4):
            RANK = discord.Embed(title=f"💯 {member.display_name} 💯", color=member.color)
            RANK.add_field(name=f'#{i+1}',value=name[i].encode_contents().decode("utf-8"),inline=True)
            RANK.set_image(url=image[i]['src'])
            await ctx.send(embed=RANK)
            sleep(1)
def setup(bot):
    bot.add_cog(ranker(bot))
