from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начало работы"
        ),
        BotCommand(
            command="help",
            description="Помощь"
        ),
        BotCommand(
            command="registration",
            description="Регистрация в боте"
        ),
        BotCommand(
            command="journal",
            description="Перейти в журнал"
        ),
        BotCommand(
            command="homework",
            description="Домашнее задание",
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

