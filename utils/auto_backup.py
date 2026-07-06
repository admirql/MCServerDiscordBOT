from mcrcon import MCRcon
import subprocess
import config

BACKUP_SCRIPT = "/home/opc/scripts/backup.sh"

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

    if result.returncode == 0:
        print("Backup completed.")
    else:
        print(result.stderr)

except Exception as e:
    print(e)