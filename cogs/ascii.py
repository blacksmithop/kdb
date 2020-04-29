import asyncio
import discord
import random
from   discord.ext import commands
from   cogs.Addons import DL
import urllib

def setup(bot):
	bot.add_cog(Ascii(bot))
	
class Ascii(commands.Cog):
    
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def asc(self, ctx, *, text : str = None):
		"""Beautify some text (font list at http://artii.herokuapp.com/fonts_list)."""

		if text == None:
			await ctx.channel.send('Usage: `{}ascii [font (optional)] [text]`\n(font list at http://artii.herokuapp.com/fonts_list)'.format(ctx.prefix))
			return

		fonturl = "http://artii.herokuapp.com/fonts_list"
		response = await DL.async_text(fonturl)
		fonts = response.split()

		font = None
		parts = text.split()
		if len(parts) > 1:
			if parts[0] in fonts:
				font = parts[0]
				text = ' '.join(parts[1:])
	
		url = "http://artii.herokuapp.com/make?{}".format(urllib.parse.urlencode({'text':text}))
		if font:
			url += '&font={}'.format(font)
		response = await DL.async_text(url)
		await ctx.channel.send("```Markup\n{}```".format(response))
