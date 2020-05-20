from discord.ext import commands
from random import choice

bot = commands.AutoShardedBot(command_prefix='..', pm_help=None, description='bot', shard_count=1)


@bot.event
async def on_message(message):
    emoji = [
        "😀", "😛", "😈", "👻", "💩", "😸", "🕸", "⚽", "🥇", "🧿", "🧲", "📳", "🎥", "📕", "🖋",
        "⏰", "🍔", "🌭", "🍿", "🥨", "🍛", "🍧", "🚓", "🚗", "🦽", "🛹", "🚲", "⚓", "☮", "🆎", "🔞", "✅"
    ]

    mentioned = message.mentions

    for i in mentioned:
        if str(i) == 'abhi#1571':
            await message.add_reaction(choice(emoji))
            break

    if 'abhi' in message.content or "ABHI" in message.content:
        await message.add_reaction(choice(emoji))
