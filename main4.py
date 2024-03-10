import asyncio
from os import getenv
from aiogram import Bot, Dispatcher, types
from dotenv import find_dotenv, load_dotenv

from handlers4.user_group import user_group_router
from handlers4.user_private import user_private_router
from common4.bot_cmds_list import private


load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['massage, edite_message']

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)  # группа на втором месте, чтоб все сообщения не перехватывались

async def main():
    # await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    # Для удаления или изменения списка команд в меню
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
