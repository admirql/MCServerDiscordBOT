import discord
from discord import app_commands
from mcrcon import MCRcon
import config

@app_commands.command(
    name="players",
    description="オンラインプレイヤー一覧"
)
async def players(interaction: discord.Interaction):

    try:
        with MCRcon(
            config.RCON_HOST,
            config.RCON_PASSWORD,
            port=config.RCON_PORT
        ) as mcr:

            players = mcr.command("list")

        await interaction.response.send_message(
            f"```{players}```"
        )

    except Exception as e:
        await interaction.response.send_message(
            f"❌ RCON接続失敗\n```{e}```"
        )