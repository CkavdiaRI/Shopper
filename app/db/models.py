import enum 
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class State(enum.Enum):
    ACTIVE= "ACTIVE"
    INACTIVE = "INACTIVE"

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[State] = mapped_column(default=State.ACTIVE)


class Category(Base):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(String(100))


class Product(Base):
    __tablename__ = "product"

    title: Mapped[str] = mapped_column(String(200))
    price: Mapped[Decimal] = mapped_column(Numeric(19, 2))
    stock: Mapped[int]
    category_id: Mapped[int | None] = mapped_column(ForeignKey("category.id"))
    category: Mapped[Category | None] = relationship()