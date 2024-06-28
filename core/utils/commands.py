from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начало работы"
        ),
        BotCommand(
            command="add_exercise",
            description="Добавить упражнение"
        ),
        BotCommand(
            command="add_photo",
            description="Добавить фото"
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

