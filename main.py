import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

from config import API_HOST, API_PORT, BOT_TOKEN, WEBAPP_URL
from db import init_db
from server import create_app

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="🎁 Открыть кейс", web_app=WebAppInfo(url=WEBAPP_URL))
    await message.answer(
        "Привет! Крути кейс и лови ценные предметы 🎰\n"
        "Каждому новому игроку — стартовый баланс монет.",
        reply_markup=builder.as_markup(),
    )


async def start_bot_polling() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def start_api_server() -> None:
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, API_HOST, API_PORT)
    await site.start()
    logging.info("API server started on %s:%s", API_HOST, API_PORT)


async def main() -> None:
    await init_db()
    await asyncio.gather(start_bot_polling(), start_api_server())


if __name__ == "__main__":
    asyncio.run(main())
