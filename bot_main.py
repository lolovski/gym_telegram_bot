import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv
from core.database.models import async_main
dot = load_dotenv('.env')

API_TOKEN = os.getenv('TOKEN_API')
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    await async_main()
    dp = Dispatcher()

    from core.handlers.basic import router
    dp.include_router(router)

    from core.handlers.exercises import router
    dp.include_router(router)

    from add_photos import router
    dp.include_router(router)

    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run((main()))


