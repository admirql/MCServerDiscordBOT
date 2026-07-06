import discord
from discord import app_commands
import subprocess
from datetime import datetime
from mcrcon import MCRcon
import config


@app_commands.command(
    name="status",
    description="Minecraftサーバーの状態"
)
async def status(interaction: discord.Interaction):

    # 状態確認
    result = subprocess.run(
        ["systemctl", "is-active", "minecraft"],
        capture_output=True,
        text=True
    )

    state = result.stdout.strip()

    if state != "active":
        await interaction.response.send_message(
            "🔴 **Minecraft Server**\n"
            "状態：停止中"
        )
        return

    # 起動時刻取得
    uptime = subprocess.run(
        [
            "systemctl",
            "show",
            "minecraft",
            "--property=ActiveEnterTimestamp"
        ],
        capture_output=True,
        text=True
    ).stdout.strip()

    start_time = uptime.split("=", 1)[1]

    dt = datetime.strptime(
        start_time,
        "%a %Y-%m-%d %H:%M:%S %Z"
    )

    elapsed = datetime.now() - dt.replace(tzinfo=None)

    hours = elapsed.seconds // 3600
    minutes = (elapsed.seconds % 3600) // 60

    # プレイヤー数
    with MCRcon(
        config.RCON_HOST,
        config.RCON_PASSWORD,
        port=config.RCON_PORT
    ) as mcr:

        players = mcr.command("list")

    # 例:
    # There are 2 of a max of 20 players online: Steve, Alex

    await interaction.response.send_message(
        f"""🟢 **Minecraft Server**

📡 状態：起動中
⏱ 起動時間：{elapsed.days}日 {hours}時間 {minutes}分
👥 {players}
"""
    )