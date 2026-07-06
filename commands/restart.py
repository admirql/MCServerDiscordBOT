import discord
from discord import app_commands

from utils.mc import systemctl
from utils.rcon import wait_for_rcon
from utils.backup import backup_world


@app_commands.command(
    name="restart",
    description="Minecraftサーバーを再起動"
)
async def restart(interaction: discord.Interaction):

    await interaction.response.send_message(
        "🟡 Minecraftサーバーを再起動しています..."
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

    # 再起動
    result = systemctl("restart")

    if result.returncode != 0:
        await interaction.followup.send(
            f"❌ 再起動失敗\n```{result.stderr}```"
        )
        return

    if await wait_for_rcon():
        await interaction.followup.send(
            "🟢 バックアップ後、Minecraftサーバーの再起動が完了しました！"
        )
    else:
        await interaction.followup.send(
            "⚠️ 再起動しましたがRCONへ接続できません。"
        )