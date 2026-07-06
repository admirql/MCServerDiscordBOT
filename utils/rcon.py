import asyncio
from mcrcon import MCRcon
import config

async def wait_for_rcon(timeout=180):

    for _ in range(timeout // 5):
        try:
            with MCRcon(
                config.RCON_HOST,
                config.RCON_PASSWORD,
                port=config.RCON_PORT
            ) as mcr:

                mcr.command("list")
                return True

        except Exception as e:
            print(e)
            await asyncio.sleep(5)

    return False