import asyncio
import re
import discord
import config


LOG_FILE = "/home/opc/minecraft/logs/latest.log"


async def log_monitor(bot):

    await bot.wait_until_ready()

    channel = bot.get_channel(config.LOG_CHANNEL_ID)

    with open(LOG_FILE, "r", encoding="utf-8") as f:

        # 起動時は最新まで読み飛ばす
        f.seek(0, 2)

        while not bot.is_closed():

            line = f.readline()

            if not line:
                await asyncio.sleep(0.5)
                continue

            # ---------- Join ----------
            m = re.search(r": ([^\s]+) joined the game", line)
            if m:
                await channel.send(
                    f"🟢 **{m.group(1)}** が参加しました"
                )
                continue

            # ---------- Left ----------
            m = re.search(r": ([^\s]+) left the game", line)
            if m:
                await channel.send(
                    f"🔴 **{m.group(1)}** が退出しました"
                )
                continue

            # ---------- Advancement ----------
            if (
                "has made the advancement" in line
                or "has completed the challenge" in line
                or "has reached the goal" in line
            ):

                msg = line.split(": ", 1)[1]

                await channel.send(
                    f"🏆 {msg}"
                )

                continue

            # ---------- Death ----------
            if (
                " was " in line
                or " fell " in line
                or " drowned " in line
                or " blew up" in line
                or " burned " in line
                or " hit the ground" in line
                or " tried to swim" in line
            ):

                msg = line.split(": ", 1)[1]

                await channel.send(
                    f"☠️ {msg}"
                )