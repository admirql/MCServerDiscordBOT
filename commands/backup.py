import discord
from discord import app_commands

from utils.backup import backup_world


@app_commands.command(
    name="backup",
    description="Minecraftワールドをバックアップします"
)
async def backup(interaction: discord.Interaction):

    await interaction.response.send_message(
        "💾 バックアップを開始しています..."
    )

    result = backup_world()

    if isinstance(result, Exception):
        await interaction.followup.send(
            f"❌ バックアップ失敗\n```{result}```"
        )
        return

    if result.returncode != 0:
        await interaction.followup.send(
            f"❌ バックアップ失敗\n```{result.stderr}```"
        )
        return

    await interaction.followup.send(
        f"✅ バックアップが完了しました。\n```{result.stdout}```"
    )