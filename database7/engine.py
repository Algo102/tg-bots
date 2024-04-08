import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database7.models import Base


# DB_LITE=sqlite+aiosqlite:///my_base.db
# DB_URL=postgresql+asyncpg://login:password@localhost:5432/db_name
# engine = create_async_engine(os.getenv("DB_LITE"), echo=True)
engine = create_async_engine(os.getenv("DB_URL"), echo=True)  # echo=True Чтоб запросы выводились в терминал

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# expire_on_commit=False чтоб сессия не закрывалась и ей можно было пользоваться повторно


# Подтягиваются и создаются все таблицы в базе данных
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Если будет необходимость удалить все таблицы из БД
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
