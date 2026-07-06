import discord
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

    if await wait_for_rcon():
        await interaction.followup.send(
            "🟢 Minecraftサーバーの起動が完了しました！"
        )
    else:
        await interaction.followup.send(
            "⚠️ 起動しましたがRCONへ接続できません。"
        )