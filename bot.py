import discord
from discord.ext import commands

import config

from commands.start import start
from commands.stop import stop
from commands.restart import restart
from commands.status import status
from commands.say import say
from commands.players import players
from commands.backup import backup
from utils.log import log_monitor


intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

guild = discord.Object(id=config.GUILD_ID)

bot.tree.add_command(start, guild=guild)
bot.tree.add_command(stop, guild=guild)
bot.tree.add_command(restart, guild=guild)
bot.tree.add_command(status, guild=guild)
bot.tree.add_command(players, guild=guild)
bot.tree.add_command(say, guild=guild)
bot.tree.add_command(backup, guild=guild)

@bot.event
async def on_ready():

    await bot.tree.sync(guild=guild)

    bot.loop.create_task(log_monitor(bot))

    print(f"Logged in as {bot.user}")

bot.run(config.TOKEN)