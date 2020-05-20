from os import environ as e
from redis import Redis
from discord import Embed, Member
from requests import get
from ast import literal_eval as l
from random import shuffle as s
from asyncio import TimeoutError
from discord.ext import commands
from json import loads, dumps
from datetime import datetime as dt

rdb = Redis(
    host=e["host"],
    port=17489,
    password=e["pwd"])


def UserSchema(member: Member, action: str = None, amt: int = None, task: str = None, nick: str = None,
               recipient: Member = None):
    if action == "add":
        user = {
            "nick": [],
            "bal": amt,
            "daily": None
        }
        if task == "prize":
            bal = UserSchema(member=member, action="get", task="getbal")
            user = loads(rdb.get(member.id))
            user["bal"] += amt
        juser = dumps(user)
        rdb.set(member.id, juser)
    if action == "transact":
        bal1 = UserSchema(member=member, action="get", task="getbal")
        bal2 = UserSchema(member=recipient, action="get", task="getbal")
        u1 = loads(rdb.get(member.id))
        u2 = loads(rdb.get(recipient.id))
        if bal1 > amt:
            if task == "add":
                u1["bal"] = bal1 - amt
                u2["bal"] = bal2 + amt
                rdb.set(member.id, dumps(u1))
                rdb.set(recipient.id, dumps(u2))
                return True
        else:
            return False
    if action == "get":
        if task == "nickget":
            user = loads(rdb.get(member.id))
            return user["nick"]
        if task == "nickadd":
            user = loads(rdb.get(member.id))
            user["nick"].append(nick)
            juser = dumps(user)
            rdb.set(member.id, juser)
        if task == "getbal":
            user = rdb.get(member.id)
            if user is None and not member.bot:
                UserSchema(member=member, action="add", amt=10)
                user = rdb.get(member.id)
            user = loads(user)
            return user["bal"]

    if action == "daily":
        bal = UserSchema(member=member, action="get", task="getbal")
        user = loads(rdb.get(member.id))
        date = dt.now()
        then = user["daily"]
        if then is None:
            then = date.strftime('%Y-%m-%d')
        then = dt.strptime(then, '%Y-%m-%d')
        if user["daily"] is None or (date - then).days >= 1:
            user["daily"] = date.strftime('%Y-%m-%d')
            user["bal"] += 25
            rdb.set(member.id, dumps(user))
            return "done"
        else:
            t = date - then
            return int(t.seconds / 3600 + t.microseconds / 3.6e+9)


def cb(arg=None):
    if arg is None:
        return "```Text Here```"
    return f"```{arg}```"


class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bal(self, ctx, member: Member = None):
        if member is None:
            member = ctx.author
        amt = UserSchema(member=member, action="get", task="getbal")
        await ctx.send(embed=Embed(title=member.display_name, description=cb(f"Balance: {amt} 🥥"), color=member.color))

    @commands.command()
    async def give(self, ctx, amt: int, member: Member = None):
        if UserSchema(member=ctx.author, recipient=member, amt=amt, action="transact", task="add"):
            await ctx.send(embed=Embed(title="Transaction 🥥",
                                       description=cb(
                                           f"{ctx.author.display_name} gave {amt} 🥥 to {member.display_name}")
                                       ))
        else:
            await ctx.send(cb("Insufficient Balance"))

    @commands.command()
    async def daily(self, ctx, member: Member = None):
        member = ctx.author
        result = UserSchema(member=member, action="daily")
        if result == "done":
            await ctx.send(embed=Embed(
                title="Claimed Daily",
                description=cb(f"{member.display_name} claimed 25 🥥!")
            ))
        else:
            await ctx.send(cb(f"Please wait {result} hours"))

    @commands.command()
    async def lb(self, ctx):
        lead = dict()
        for user in ctx.guild.members:
            if not user.bot:
                bal = UserSchema(member=user, action="get", task="getbal")
                if bal is not None:
                    lead[user.id] = bal
                    print("...")
        lead = {k: v for k, v in sorted(lead.items(), key=lambda item: item[1])}
        top = list(lead.keys())
        top = list(reversed(top))
        board = ""
        for i in range(10):
            user = self.bot.get_user(top[i])
            board += f"{i + 1})  **{user.display_name}** {lead[top[i]]} 🥥\n\n"
        await ctx.send(
            embed=Embed(
                title=f"Leaderboard for {ctx.guild.name}", description=board, color=ctx.author.color))

    @commands.command()
    async def trivia(self, ctx):
        q = get("https://opentdb.com/api.php?amount=1").content.decode("utf-8")
        q = l(q)['results'][0]
        Tr = Embed()
        Tr.title = q["question"].replace("&quot;", "'").replace("&#039;", "'")
        opt = q["incorrect_answers"]
        opt.append(q["correct_answer"])
        s(opt)

        if q["type"] == "multiple":
            Tr.description = f"```A) {opt[0]}\nB) {opt[1]}\nC) {opt[2]}\nD) {opt[3]}```"
            mcq = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8", "\U0001F1E9"]
            o2e = dict(zip(opt, mcq))

        if q["type"] == "boolean":
            Tr.description = f"```1) True\n2) False```"
            mcq = ["\U0001F1F9", "\U0001F1EB"]
            o2e = {"True": mcq[0], "False": mcq[1]}

        mess = await ctx.send(embed=Tr)
        for emoji in mcq:
            await mess.add_reaction(emoji)
        ans = {"R": {*()}, "W": {*()}}
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0)
                em = str(reaction.emoji)
            except TimeoutError:
                await ctx.send(content="```Time's up ⌚!```")
                break
            if em == o2e[q["correct_answer"]] and user != self.bot.user:
                ans["R"].add(user.id)
            else:
                ans["W"].add(user.id)
        await ctx.send(content=f"```Correct answer was {q['correct_answer']}```")
        for right in ans["R"]:
            if right not in ans["W"]:
                await ctx.send(f"<@{right}> won 10 🥥")
                UserSchema(member=self.bot.get_user(right), action="add", task="prize", amt=10)


def setup(bot):
    bot.add_cog(economy(bot))
