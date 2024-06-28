from aiogram import types, Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
import os
from core.keyboards import reply
from ..utils.commands import set_commands


admin_id = '6494107709'

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: types.Message):
    try:

        await message.answer(f'<b>Добро пожаловать в GymBot, {message.from_user.first_name}!</b>', reply_markup=reply.start)
    except:
        await message.answer(f'<b>Добро пожаловать в GymBot!</b>',
                             reply_markup=reply.start)

@router.startup()
async def on_startup(bot: Bot):
    await set_commands(bot)
    await bot.send_message(admin_id, text=f'<tg-spoiler>Начало работы</tg-spoiler>')


@router.shutdown()
async def on_shutdown(bot: Bot):
    await bot.send_message(admin_id, text='Прекращение работы!')

