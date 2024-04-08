# Промежуточный слой между базой данных и роутером, но также
# можно вешать на корневой диспетчер
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.sessions_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.sessions_pool() as session:
            data['session'] = session
            return await handler(event, data)

# # Обязательно наследуемся от BaseMiddleware
# # __init__ отрабатывает один раз при старте бота при регистрации Middleware слоя
# class CounterMiddleware(BaseMiddleware):
#     def __init__(self) -> None:
#         self.counter = 0
#
#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#         event: Message,
#         data: Dict[str, Any]  # Словарь в котором содержаться данные, которые могут передаваться в хендлер
#     ) -> Any:
#         self.counter += 1
#         data['counter'] = self.counter
#         return await handler(event, data)
# # Чтоб все работало, обязательно вызывается handler, если предварительно
# # провести проверку пользователя (к примеру он забанен) и при необходимости не
# # доводить до handler, то update будет считаться дропнутым
