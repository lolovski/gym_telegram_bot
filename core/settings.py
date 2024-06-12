from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id : str


@dataclass
class Settings:

    bots: Bots


def get_settings(path: str) -> Settings:
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN_API"),
            admin_id=env.str("ADMIN_ID")
        )
    )


settings = get_settings("../.env")
print(settings)
print(settings.bots.bot_token)