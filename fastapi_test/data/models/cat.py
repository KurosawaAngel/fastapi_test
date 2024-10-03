from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Cat(Base):
    __tablename__ = "cats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    color: Mapped[str]
    months: Mapped[int]
    breed: Mapped[str]
    description: Mapped[str]
