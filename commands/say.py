import discord
from discord import app_commands
from mcrcon import MCRcon
import config

@app_commands.command(
    name="say",
    description="ゲーム内へメッセージ送信"
)
@app_commands.describe(message="送信するメッセージ")
async def say(
    interaction: discord.Interaction,
    message: str
):

    try:
        with MCRcon(
            config.RCON_HOST,
            config.RCON_PASSWORD,
            port=config.RCON_PORT
        ) as mcr:

            mcr.command(f"say {message}")

        await interaction.response.send_message(
            "✅ メッセージを送信しました。"
        )

    except Exception as e:
        await interaction.response.send_message(
            f"❌ {e}"
        )