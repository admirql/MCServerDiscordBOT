import discord
import config
from discord import app_commands

from utils.mc import systemctl
from utils.backup import backup_world


@app_commands.command(
    name="stop",
    description="Minecraftサーバーを停止します"
)
async def stop(interaction: discord.Interaction):

    await interaction.response.send_message(
        "🛑 サーバーを停止しています..."
    )

    # バックアップ
    backup = backup_world()

    if isinstance(backup, Exception):
        await interaction.followup.send(
            f"❌ バックアップ失敗\n```{backup}```"
        )
        return

    if backup.returncode != 0:
        await interaction.followup.send(
            f"❌ バックアップ失敗\n```{backup.stderr}```"
        )
        return

    # サーバー停止
    result = systemctl("stop")

    if result.returncode != 0:
        await interaction.followup.send(
            f"❌ 停止失敗\n```{result.stderr}```"
        )
        return

    channel = interaction.client.get_channel(config.LOG_CHANNEL_ID)

    if channel:
        await channel.send("🔴 Minecraftサーバーが停止しました。")