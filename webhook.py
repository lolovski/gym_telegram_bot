import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import nest_asyncio
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv
from core.database.models import async_main
dot = load_dotenv('.env')

API_TOKEN = os.getenv('TOKEN_API')
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
WEBHOOK_HOST = "https://gymbot.alwaysdata.net"
WEBHOOK_PATH = "gym_telegram_bot"
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = '::'
WEBAPP_PORT = 8350

nest_asyncio.apply()


async def main() -> None:
    await async_main()
    dp = Dispatcher()

    from core.handlers.basic import router
    dp.include_router(router)

    from core.handlers.exercises import router
    dp.include_router(router)

    from add_photos import router
    dp.include_router(router)

    from core.handlers.AI_assistant import router
    dp.include_router(router)

    from core.handlers.db_add_info import router
    dp.include_router(router)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)

    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run((main()))


