import subprocess

SERVICE_NAME = "minecraft"

def systemctl(action: str):
    return subprocess.run(
        ["sudo", "systemctl", action, SERVICE_NAME],
        capture_output=True,
        text=True
    )