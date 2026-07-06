import discord
import asyncio
import subprocess
from mcrcon import MCRcon
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
    print(f"Logged in as {bot.user}")

    bot.loop.create_task(update_presence())

    await bot.tree.sync(guild=guild)

    bot.loop.create_task(log_monitor(bot))

async def update_presence():
    await bot.wait_until_ready()

    while not bot.is_closed():

        try:
            with MCRcon(
                config.RCON_HOST,
                config.RCON_PASSWORD,
                port=config.RCON_PORT
            ) as mcr:

                result = mcr.command("list")

            if ": " in result:
                players = result.split(": ", 1)[1].strip()
                count = len(players.split(",")) if players else 0

                if count == 0:
                    await bot.change_presence(
                        activity=discord.Game("🟢 サーバー起動中")
                    )
                else:
                    await bot.change_presence(
                        activity=discord.Game(f"👥 {count}人プレイ中")
                    )

        except Exception:
            await bot.change_presence(
                activity=discord.Game("🔴 サーバー停止中")
            )

        await asyncio.sleep(30)

bot.run(config.TOKEN)