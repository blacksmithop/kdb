from imdb import IMDb
from discord import Embed
from re import search

from discord.ext import commands



class movies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='movie', aliases=['mov'])
    @commands.guild_only()
    async def get_movie(self, ctx, args):
        ia = IMDb()
        movie_embed = Embed()
        movie_embed = handle(args, ia, movie_embed)
        await ctx.send(embed=movie_embed)


def setup(bot):
    bot.add_cog(movies(bot))


def handle(movie_name, ia, movie_embed):
    # say('Searching top five results for.  %s' %movie_name)
    movie_query = ia.search_movie(movie_name)
    del movie_query[5:]
    for movie in movie_query:
        # say('Did you mean %s (%s)?' % (movie.get('title'), movie.get('year')))
        # response = Listen()
        # if yes(response):
        ia.update(movie)
        info = f" {movie.get('title')} - {movie.get('year')}"
        movie_embed.title = info
        if movie.get('cover url'):
            movie_embed.set_image(url=movie.get('cover url'))
        if movie.get('rating'):
            info = f"Rating: {movie.get('rating')}/10.  "
            movie_embed.add_field(name="\u200b", value=info, inline=False)
        if movie.get('runtimes'):
            info = f"Runtime: {movie.get('runtimes')[0]} mins "
            movie_embed.add_field(name="\u200b", value=info, inline=False)
        if movie.get('genres'):
            info = 'Genres :%s  ' % ','.join(movie.get('genres'))
            movie_embed.add_field(name="\u200b", value=info, inline=False)
        if movie.get('director'):
            info = f"Directors{movie.get('director')}"
            info = search(r'name:(.*?)>', info).group(1)
            info = f"Directed by: {info}"
            movie_embed.add_field(name="\u200b", value=info, inline=False)
        # if movie.get('producer'):
        # info = f"Producers.  {movie.get('producer')}  "
        # movie_embed.add_field(name="\u200b", value=info, inline=False)
        # if movie.get('cast'):
        # #info = f"Cast.  {movie.get('cast')}"
        # movie_embed.add_field(name="\u200b", value=info, inline=False)
        break
    return movie_embed
