from mcrcon import MCRcon
import subprocess
import config

BACKUP_SCRIPT = "/home/opc/scripts/backup.sh"

def backup_world():

    try:
        with MCRcon(
            config.RCON_HOST,
            config.RCON_PASSWORD,
            port=config.RCON_PORT
        ) as mcr:

            mcr.command("save-off")
            mcr.command("save-all flush")

            result = subprocess.run(
                [BACKUP_SCRIPT],
                capture_output=True,
                text=True
            )

            mcr.command("save-on")

        return result

    except Exception as e:
        return e