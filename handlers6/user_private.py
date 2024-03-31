from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from filters6.chat_types import ChatTypeFilter
from kbds6.reply import get_keyboard
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from filters6.chat_types import ChatTypeFilter


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        'Привет, я виртуальный помощник',
        reply_markup=get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            placeholder="Что вас интересует?",
            sizes=(2, 2)
        ),
    )



# Создали клавиатуру через Markup
# @user_private_router.message(CommandStart())
# async def start_cmd(message: types.Message):
#     # start_kb = ReplyKeyboardMarkup(  # Можно разместить здесь,  а не в reply, но запись будет массивной
#     #     keyboard=[
#     #         [
#     #             KeyboardButton(text="Меню"),
#     #             KeyboardButton(text="О магазине"),
#     #         ],
#     #         [
#     #             KeyboardButton(text="Варианты доставки"),
#     #             KeyboardButton(text="Варианты оплаты"),
#     #         ],
#     #     ],
#     #     resize_keyboard=True,
#     #     input_field_placeholder='Что Вас интересует?'
#     # )
#     # await message.answer('Привет, я виртуальный помощник', reply_markup=start_kb)
#     await message.answer('Привет, я виртуальный помощник', reply_markup=reply.start_kb)


# Вызываем клавиатуру созданную другим классом через Builder
# @user_private_router.message(CommandStart())
# async def start_cmd(message: types.Message):
#     await message.answer('Привет, я виртуальный помощник',
#                          reply_markup=reply.start_kb2.as_markup(
#                              resize_keyboard=True,
#                              input_field_placeholder='Что Вас интересует?'))


# # Вызываем клавиатуру Builder теже кнопки + дополнительная
# @user_private_router.message(CommandStart())
# async def start_cmd(message: types.Message):
#     await message.answer('Привет, я виртуальный помощник',
#                          reply_markup=reply.start_kb3.as_markup(
#                              resize_keyboard=True,
#                              input_field_placeholder='Что Вас интересует?'))



# @user_private_router.message(F.text.lower() == 'меню')  # or_f ч/з запятую, работает как or
@user_private_router.message(or_f(Command('menu'), (F.text.lower() == 'меню')))
# @user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    # при вызове меню, можно удалить клавиатуру
    # await message.answer('Вот меню', reply_markup=reply.del_kbd)
    await message.answer('Вот меню')


@user_private_router.message(F.text.lower() == 'о магазине')
@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('О нас')


@user_private_router.message(F.text.lower() == 'варианты оплаты')
@user_private_router.message(Command('payment'))
async def payment_cmd(message: types.Message):

    text = as_marked_section(
        Bold('Варианты оплаты:'),
        'Картой в боте',
        'При получении карта/кеш',
        'В заведении',
        marker='✅ '
    )
    await message.answer(text.as_html())


@user_private_router.message((F.text.lower().contains('заказ')) | (F.text.lower() == 'варианты доставки'))
@user_private_router.message(Command('shipping'))
async def shipping_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold('Варианты доставки/заказа:'),
            'Курьер',
            'Самовынос (сейчас прибегу и заберу)',
            'Покушаю у Вас (сейчас прибегу)',
            marker='✅ '
        ),
        as_marked_section(
            Bold('Нельзя:'),
            'Почта',
            'Голуби',
            marker='❌ '
        ),
        sep='\n-----------------------\n'
    )
    await message.answer(text.as_html())
    # await message.answer('<b>Доставка</b>')
    # Чтоб парсмод не указывать в каждом хендлере, пишем его один раз в стартовом БОТ
    # await message.answer('<b>Доставка</b>', parse_mode=ParseMode.HTML)


@user_private_router.message(Command('exit'))
async def exit_cmd(message: types.Message):
    await message.answer('Выход')

# F.from_user.id == 42  # можно сравнивать с номером юзера, если ровно
# F.text != 'spam'  # если не ровно
# F.from_user.id.in_({42, 1000, 123123})  # один из
# F.data.in_({'foo', 'bar', 'baz'})  # один из
# F.text.contains('foo')  # содержит
# F.text.startswith('foo')  # Строка начинается/заканчивается
# F.text.endswith('bar')  # применяться только для текстовых атрибутов
# ~F.text  # Инвертирование
# ~F.text.startswith('spam')
# F.text.lower() == 'test'  # Манипуляции со строками
# F.text.upper().in_({'FOO', 'BAR'})
# F.text.len() == 5


# @user_private_router.message(F.text, F.text.lower() == 'варианты доставки')  # Запятая и & это И. | и or_f ч/з, - или
# @user_private_router.message((F.text.lower().contains('ну')) | (F.text.lower() == 'варианты доставки'))
# async def ship1_cmd(message: types.Message):
#     await message.answer('Это магический фильтр0')


# @user_private_router.message(F.text.lower() == 'варианты доставки')
# async def ship1_cmd(message: types.Message):
#     await message.answer('Это магический фильтр1')
#
#
@user_private_router.message(F.text.lower().contains('варианты доставки'))
async def ship2_cmd(message: types.Message):
    await message.answer('Это магический фильтр2')


@user_private_router.message((F.text == 'Саша') | (F.text == 'Александр'))
async def ship2_cmd(message: types.Message):
    await message.answer(f'Привет {message.text}')


# @user_private_router.message(F.text)  # вместо text можно написать photo, audio, sticker
# async def all_cmd(message: types.Message):
#     await message.answer('Пиши хоть что')


@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f'номер получен')
    await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f'локация получена')
    await message.answer(str(message.location))
