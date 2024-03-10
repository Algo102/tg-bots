from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from filters4.chat_types import ChatTypeFilter


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник, как тебя зовут?')


# @user_private_router.message(F.text.lower() == 'меню')  # or_f ч/з запятую, работает как or
@user_private_router.message(or_f(Command('menu'), (F.text.lower() == 'меню')))
@user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer('Вот меню')


@user_private_router.message(F.text.lower() == 'о нас')
@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('О нас')


@user_private_router.message(F.text.lower() == 'варианты оплаты')
@user_private_router.message(Command('payment'))
async def payment_cmd(message: types.Message):
    await message.answer('Оплата')


@user_private_router.message((F.text.lower().contains('заказ')) | (F.text.lower() == 'варианты доставки'))
@user_private_router.message(Command('shipping'))
async def shipping_cmd(message: types.Message):
    await message.answer('Доставка')


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

