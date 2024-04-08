import asyncio
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from middlewares7.db import DataBaseSession
from database7.engine import create_db, drop_db, session_maker
# from middlewares7.db import CounterMiddleware
from handlers7.user_private import user_private_router
from handlers7.user_group import user_group_router
from handlers7.admin_private import admin_router
from common7.bot_cmds_list import private

# ALLOWED_UPDATES = ['massage', 'edite_message', 'callback_query']

bot = Bot(token=getenv('TOKEN'),
          parse_mode=ParseMode.HTML)  # This arguments will be removed in 3.5.0 version. Но пока работает
# bot = Bot(token=getenv('TOKEN'))
bot.my_admins_list = []

dp = Dispatcher()

# # # outer_middleware - работает до фильтрации, к примеру, админ не войдя
# # # в систему может производить действия, которые сработают после входа
# # admin_router.message.outer_middleware(CounterMiddleware())
#
# # middleware - работает после фильтрации
# admin_router.message.middleware(CounterMiddleware())

dp.include_router(user_private_router)
dp.include_router(user_group_router)  # группа на втором месте, чтоб все сообщения не перехватывались
dp.include_router(admin_router)


async def on_startup(bot):
    # Если нужно сбросить все таблицы перед запуском ставим True
    run_param = False
    if run_param:
        await drop_db()
    # Если таблицы уже есть то create_db() ничего делать не будет
    await create_db()


async def on_shutdown(bot):
    print('бот лег ...')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    # Для удаления или изменения списка команд в меню убрать подгрузку
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    # Для удаления или изменения списка команд в меню
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    # await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
