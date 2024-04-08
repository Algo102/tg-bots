# pip install sqlalchemy
# pip install aiosqlite
# pip install asyncpg
from sqlalchemy import Float, String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Создаем основной класс от которого будут наследоваться таблицы
class Base(DeclarativeBase):
    # Во всех созданных таблицах будут поля с текущем временем, создания и обновления записи
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


# класс который будет описывать таблицу продуктов
class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    image: Mapped[str] = mapped_column(String(150))