import asyncio
from os import getenv
from aiogram import Bot, Dispatcher, types

# Две строки ниже, если не в пайчарм, где нужно создавать вирт.окружение
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from handlers3_1.user_private import user_private_router

ALLOWED_UPDATES = ['massage, edite_message']

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(user_private_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
