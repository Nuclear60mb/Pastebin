from datetime import date
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(30), nullable=True)
    user_bio: Mapped[str] = mapped_column(String(1024), nullable=True)
    live: Mapped[str] = mapped_column(String(1024), nullable=True)
    gender: Mapped[str] = mapped_column(String(1024), nullable=True)
    birthday: Mapped[date] = mapped_column(nullable=True)

    posts_count: Mapped[int] = mapped_column(Integer, nullable=True)