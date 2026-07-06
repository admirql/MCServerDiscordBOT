import discord

import config

from discord import app_commands

from utils.mc import systemctl
from utils.rcon import wait_for_rcon


@app_commands.command(
    name="start",
    description="Minecraftサーバーを起動"
)
async def start(interaction: discord.Interaction):

    await interaction.response.send_message(
        "🟡 Minecraftサーバーを起動しています..."
    )

    result = systemctl("start")

    if result.returncode != 0:
        await interaction.followup.send(
            f"❌ 起動失敗\n```{result.stderr}```"
        )
        return

    channel = interaction.client.get_channel(config.LOG_CHANNEL_ID)

    if  channel:
        await channel.send("🟢 Minecraftサーバーが起動しました。")
    else:
        await interaction.followup.send(
            "⚠️ 起動しましたがRCONへ接続できません。"
        )