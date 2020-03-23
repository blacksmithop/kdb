import numpy as np
from discord import Embed
from time import sleep


class OKP(object):
    player_num: int

    def __init__(self, player_num=2, test=None):

        if test is None:
            self.player_num = player_num
            self.player_names = [None] * player_num
            # self.add_players()
        else:
            self.player_num = 2
            self.player_names = ['A', 'B']

        self.game_board = np.ones((self.player_num, 5))
        self.row_pointer = None
        self.col_pointer = None
        self.rc = None
        self.num = None

    def add_players(self, list_of_players):
        # for i in range(self.player_num):
        # print(f"Enter Member {i + 1}")
        # self.player_names[i] = input()
        self.player_names = list_of_players

    def get_player_list(self):
        return self.player_names

    def get_board(self):
        return self.game_board

    def check_game(self):
        for i in range(self.player_num):
            count = 0
            for j in range(5):
                if self.game_board[i][j] == 0:
                    count += 1
            if count == 5:
                return True
                break
        return False

    def karakk(self, num, rc):

        is_counting = True
        count = 0
        self.num = num
        self.rc = rc
        while is_counting:
            self.col_pointer += 1
            if self.col_pointer > 4:
                self.col_pointer = 0
                self.row_pointer += 1
                if self.row_pointer >= self.player_num:
                    self.row_pointer = 0
            if self.game_board[self.row_pointer, self.col_pointer] == 1:
                count += 1
            if count == 13:
                is_counting = False
        if self.rc == 'r':
            return self.row_pointer
        else:
            return self.col_pointer


'''
   async def botsay(self,ctx, inp):
        sleep(1.5)
        await ctx.send(inp)
'''

from discord.ext import commands
from kdb.cogs.OKP import OKP


class kali(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='okp', aliases=['OKP'])
    @commands.guild_only()
    async def Oramma(self, ctx, *, args):
        players = args.split(',')
        OKP.player_num = len(players)
        '''
        player_to_id = {}
        player_to_id[ctx.author.display_name] = [players[0]]
        player_to_id[]'''
        oramma = OKP()
        kadal = Embed()

        kadal.title = "Oramma Kadalil Poyi!"
        game_info = f"Number of Players: {len(players)} \nPlayers are: {args}"
        kadal.description = game_info
        await ctx.send(embed=kadal)
        oramma.add_players(list_of_players=players)

        # await ctx.send(','.join(oramma.get_player_list()))
        #####################################################
        oramma.row_pointer = 0
        oramma.col_pointer = 0
        winner = ''
        oramma.get_player_list()
        sleep(0.7)
        await ctx.send(oramma.get_board())

        colormap = {}
        colormap[oramma.get_player_list()[0]] = 0x99ccff
        colormap[oramma.get_player_list()[1]] = 0xff9900

        channel = ctx.channel
        game_end = False
        while not game_end:
            game_embed = Embed()
            # 13 is taken as the number of open fingers to be moved each time Oramma is evoked.
            oramma.row_pointer = oramma.karakk(13, 'r')
            oramma.col_pointer = oramma.karakk(13, 'c')
            game_embed.description = "Oramma kadayil poyi, \nOru dazan vala vaangi, \nAa valayude niramenth?"
            await ctx.send(embed=game_embed)
            sleep(0.7)
            current_player = oramma.player_names[oramma.row_pointer]
            game_embed.description = f"{current_player}:"
            game_embed.color = colormap[current_player]
            await ctx.send(embed=game_embed)
            sleep(0.7)
            # read input here
            # c='orangeeee'
            num = await self.bot.wait_for('message', check=None)
            sleep(2)
            async for msg in channel.history(limit=1):
                c = msg.content
                print(msg.author.bot)
            game_embed.description = str(c)
            await ctx.send(embed=game_embed)
            oramma.row_pointer = oramma.karakk(len(c), 'r')
            oramma.col_pointer = oramma.karakk(len(c), 'c')
            oramma.game_board[oramma.row_pointer, oramma.col_pointer] = 0
            sleep(0.7)
            game_embed.description = str(oramma.get_board())
            await ctx.send(embed=game_embed)
            game_end = oramma.check_game()
            winner = oramma.player_names[oramma.row_pointer]  # winner will be printed only after while loop is break
            oramma.row_pointer = oramma.karakk(13, 'r')
            oramma.col_pointer = oramma.karakk(13, 'c')
            sleep(0.7)
            game_embed.description = f'Winner is {winner}'
        await ctx.send(embed=game_embed)

    @commands.command(name='getid', aliases=['gi'])
    @commands.guild_only()
    async def get_ID(self, ctx):
        await ctx.send(ctx.author.id)


def setup(bot):
    bot.add_cog(kali(bot))
