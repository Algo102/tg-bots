from string import punctuation
from aiogram import Router, types

from filters5.chat_types import ChatTypeFilter
from handlers5.rus_mat import rus_mat

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

# restricted_word = {'кабан', 'хомяк', 'выхухоль'}


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))
# maketrans - шаблон-матрица замены, что меняем, на что меняем, что вырезать


# Удаление сообщений, где содержатся слова из словаря русского мата
@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if rus_mat.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.first_name}, мат запрещен, соблюдайте порядок в чате')
        await message.delete()
        # await message.chat.ban(message.from_user.id)
