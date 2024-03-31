from string import punctuation
from aiogram import Router, types, F, Bot
from aiogram.filters import Command

from filters6.chat_types import ChatTypeFilter
from handlers6.rus_mat import rus_mat


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))
# restricted_word = {'кабан', 'хомяк', 'выхухоль'}


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    # посмотреть все данные и свойства полученных объектов
    # print(admins_list)
    # код ниже это генератор списка, как этот x = [i for i in range(10)]
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()
    # print(admins_list)


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))
# maketrans - шаблон-матрица замены, что меняем, на что меняем, что вырезать


# Удаление сообщений, где содержатся слова из словаря русского мата
@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if rus_mat.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.first_name}, соблюдайте порядок в чате')
        await message.delete()
        # await message.chat.ban(message.from_user.id)
