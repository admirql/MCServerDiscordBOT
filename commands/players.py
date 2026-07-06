import discord
from discord import app_commands
from mcrcon import MCRcon
import config


@app_commands.command(
    name="players",
    description="現在ログイン中のプレイヤー一覧"
)
async def players(interaction: discord.Interaction):

    try:
        with MCRcon(
            config.RCON_HOST,
            config.RCON_PASSWORD,
            port=config.RCON_PORT
        ) as mcr:

            result = mcr.command("list")

    except Exception:
        await interaction.response.send_message(
            "🔴 サーバーが起動していないか、RCONへ接続できません。"
        )
        return

    # 例:
    # There are 3 of a max of 20 players online: Steve, Alex, Notch

    if ": " in result:
        player_text = result.split(": ", 1)[1].strip()

        if not player_text:
            await interaction.response.send_message(
                "👥 **ログイン中のプレイヤー**\n現在オンラインのプレイヤーはいません。"
            )
            return

        player_list = [name.strip() for name in player_text.split(",")]
        count = len(player_list)

        await interaction.response.send_message(
            "👥 **ログイン中のプレイヤー**\n\n"
            f"人数：**{count}人**\n"
            "```" + "\n".join(player_list) + "```"
        )

    else:
        await interaction.response.send_message(result)