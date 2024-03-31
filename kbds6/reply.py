from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,),
):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Отправить номер телефона"
            placeholder="Что вас интересует?",
            request_contact=4,
            sizes=(2, 2, 1)
        )
    '''
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, inpute_field_placeholder=placeholder)


# # ReplyKeyboardMarkup Импортировали класс для ответной клавиатуры (1 способ)
# # ReplyKeyboardBuilder создание клавиатуры (2 способ) более гибкий вариант
# # KeyboardButton для формиования клавиатуры
# # ReplyKeyboardRemove  для удаления клавы
# # Распределили кнопки в два ряда
# start_kb = ReplyKeyboardMarkup(  # Список из списков кнопок
#     keyboard=[
#         [
#             KeyboardButton(text="Меню"),
#             KeyboardButton(text="О магазине"),
#         ],
#         [
#             KeyboardButton(text="Варианты доставки"),
#             KeyboardButton(text="Варианты оплаты"),
#         ],
#     ],
#     resize_keyboard=True,
#     input_field_placeholder='Что Вас интересует?'
# )
#
# # Если клава не нужна, можно удалить
# del_kbd = ReplyKeyboardRemove()
#
#
# # Создание клавы с помощью другого класса
# start_kb2 = ReplyKeyboardBuilder()
# start_kb2.add(
#     KeyboardButton(text="Меню"),
#     KeyboardButton(text="О магазине"),
#     KeyboardButton(text="Варианты доставки"),
#     KeyboardButton(text="Варианты оплаты"),
# )
# start_kb2.adjust(2, 2)  # Количество кнопок по рядам
#
#
# # Если нужна такая же клава, но с добавлением кнопок, то в этом классе есть для этого
# # методы, и на основе существующей добавляет новые кнопки
# start_kb3 = ReplyKeyboardBuilder()
# start_kb3.attach(start_kb2)
# # start_kb3.add(KeyboardButton(text="Оставить отзыв"),)
# # start_kb3.adjust(2, 2)
# start_kb3.row(KeyboardButton(text="Оставить отзыв"),)  # другой способ добавления новой кнопки
#
#
# test_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Создать опрос", request_poll=KeyboardButtonPollType()),
#         ],
#         [
#             KeyboardButton(text="Отправить номер", request_contact=True),
#             KeyboardButton(text="Отправить локацию", request_location=True),
#         ],
#     ],
#     resize_keyboard=True,
# )