import asyncio
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

from handlers5.user_group import user_group_router
from handlers5.user_private import user_private_router
from common5.bot_cmds_list import private


load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['massage, edite_message']

bot = Bot(token=getenv('TOKEN'), parse_mode=ParseMode.HTML)  # This arguments will be removed in 3.5.0 version. Но пока работает
# bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)  # группа на втором месте, чтоб все сообщения не перехватывались

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # Отключил голубую кнопку меню
    # await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    # Для удаления или изменения списка команд в меню
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
