import asyncio
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart


bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Эта была команда старт')

@dp.message()
async def start_cmd(message: types.Message):
# async def start_cmd(message: types.Message, bot: Bot):
# ответ именно этому пользователю, так нет смысла делать, т.к. answer итак ответ пользовалю или группе.
#     await bot.send_message(message.from_user.id, 'Ответ')
    await message.answer(message.text)  # эхо
    await message.reply(message.text)  # эхо в ответ с упоминанием автора, полезно в группах

    # text: str | None = message.text
    # if text in ['Привет', 'привет', 'hi', 'hello']:
    #     await message.answer('И тебе привет')
    # elif text in ['Пока', 'пока', 'пакеда', 'До свидания']:
    #     await message.answer('И тебе пока')
    # else:
    #     await message.answer(message.text)




async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Удалить сообщения, которые прилетали во время когда бот не работал
    await dp.start_polling(bot)

asyncio.run(main())
