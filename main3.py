import asyncio
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Эта была команда старт')

@dp.message()
async def start_cmd(message: types.Message):
    text: str | None = message.text
    await message.answer(message.text)
    await message.reply(message.text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
