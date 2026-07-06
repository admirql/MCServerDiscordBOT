import discord
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

    await interaction.followup.send(
        "✅ バックアップ後、サーバーを停止しました。"
    )