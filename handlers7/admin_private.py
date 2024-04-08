from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from database7.models import Product
from database7.orm_query import orm_add_product, orm_get_products, orm_delete_product, orm_get_product, \
    orm_update_product
from filters7.chat_types import ChatTypeFilter, IsAdmin
from kbds7.inline import get_callback_btns
from kbds7.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    # "Изменить товар",
    # "Удалить товар",
    # "Я так, просто посмотреть зашел",
    placeholder="Выберите действие",
    # sizes=(2, 1, 1),
    sizes=(2,),
)


class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        'AddProduct:name': 'Введите название заново:',
        'AddProduct:description': 'Введите описание заново:',
        'AddProduct:price': 'Введите стоимость заново:',
        'AddProduct:image': 'Этот стейт последний, поэтому',
    }


@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


# @admin_router.message(F.text == "Я так, просто посмотреть зашел")
# async def starring_at_product(message: types.Message):
#     await message.answer("ОК, вот список товаров")


@admin_router.message(F.text == "Ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
            reply_markup=get_callback_btns(btns={
                'Удалить': f'delete_{product.id}',
                'Изменить': f'change_{product.id}'
                }
            ),
        )
    await message.answer("ОК, вот список товаров")


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session, int(product_id))
    await callback.answer('Товар удален')
    await callback.message.answer('Товар удален!')


# @admin_router.message(F.text == "Изменить товар")
# async def chang_product(message: types.Message):
#     await message.answer("ОК, вот список товаров")
#
#
# @admin_router.message(F.text == "Удалить товар")
# async def delete_product(message: types.Message):
# # async def delete_product(message: types.Message, counter):
# #     print(counter)
#     await message.answer("Выберите товар(ы) для удаления")


# Становимся в состояние ожидания ввода name
@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product_callback(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    product_for_change = await orm_get_product(session, int(product_id))

    AddProduct.product_for_change = product_for_change
    await callback.answer()
    await callback.message.answer('Введите название товара', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)


# Код ниже для машины состояния (FSM)
# StateFilter(None) - хендлер, будет срабатывать если у пользователя нет активного состояния
# Становимся в состояние ожидания ввода name
@admin_router.message(StateFilter(None), F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Введите название товара", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)


# Хендлер отмены и сброса состояния, должен быть всегда именно здесь,
# после того как толь встали в состояние номер 1 (элементарная очередность фильтров)
@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddProduct.product_for_change:
        AddProduct.product_for_change=None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


# Вернуться на шаг назад (на прошлое состояние)
@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('Предидущего шага нет, или введите название товара или напишите "отмена"')
        return

    previos = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previos)
            await message.answer(f"ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previos.state]}")
            return
        previos = step


# Ловим данные для состояния name и потом меняем состояние на description
@admin_router.message(AddProduct.name, or_f(F.text, F.text == '.'))
# @admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        # Можно сделать доп проверку и выйти из хендлера не меняя сообщения
        # например:
        if len(message.text) >= 100:
            await message.answer("Название товара не должно превышать 100 символов. \n Введите заново")
            return
        await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)

    # # Можно сделать доп проверку и выйти из хендлера не меняя сообщения
    # # например:
    # if len(message.text) >= 100:
    #     await message.answer("Название товара не должно превышать 100 символов. \n Введите заново")
    #     return
    # await state.update_data(name=message.text)
    # await message.answer("Введите описание товара")
    # await state.set_state(AddProduct.description)


# Хендлер для отлова некорректных вводов для состояния name
@admin_router.message(AddProduct.name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Ввели не допустимые данные, введите текст названия товара")


# Ловим данные для состояния discription и потом меяем состояние на price
@admin_router.message(AddProduct.description, or_f(F.text, F.text == '.'))
async def add_discription(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара")
    await state.set_state(AddProduct.price)


# Хендлер для отлова некорректных вводов для состояния discription
@admin_router.message(AddProduct.description)
async def add_discription(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст описания товара")


# Ловим данные для состояния price и потом меняем состояние на image
@admin_router.message(AddProduct.price, or_f(F.text, F.text == '.'))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Введите корректное значение цены")
            return

        await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)


# Хендлер для отлова некорректных вводов для состояния price
@admin_router.message(AddProduct.price)
async def add_price(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите стоимость товара")


# [-1] самое большое разрешение у телеграма
# Ловим данные для состояния image и потом выходим из состояний
@admin_router.message(AddProduct.image, or_f(F.photo, F.text == "."))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):

    if message.text and message.text == '.':
        await state.update_data(image=AddProduct.product_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()  # Формируем словарь с товаром(добавление в каталог), перед записью в БД
    try:
        if AddProduct.product_for_change:
            await orm_update_product(session, AddProduct.product_for_change.id, data)
        else:
            await orm_add_product(session, data)
        await message.answer("Товар добавлен/изменен", reply_markup=ADMIN_KB)
        await state.clear()
    except Exception as e:
        await message.answer(f"Ошибка: \n{str(e)}\nОбратитесь к программисту", reply_markup=ADMIN_KB)
        await state.clear()

    AddProduct.product_for_change = None

    # await message.answer(str(data))

    # obj = Product(
    #     name=data['name'],
    #     description=data['description'],
    #     price=float(data['price']),
    #     image=data['image'],
    # )
    # session.add(obj)
    # await session.commit()  # Сохраняем изменения в базу данных


# Хендлер для отлова некорректных вводов для состояния image
@admin_router.message(AddProduct.image)
async def add_image(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото пиццы")
