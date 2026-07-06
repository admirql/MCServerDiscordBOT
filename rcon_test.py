from mcrcon import MCRcon
import config

try:
    with MCRcon(
        config.RCON_HOST,
        config.RCON_PASSWORD,
        port=config.RCON_PORT
    ) as mcr:
        print("RCON接続成功！")
        print(mcr.command("list"))

except Exception as e:
    print("RCON接続失敗")
    print(e)
