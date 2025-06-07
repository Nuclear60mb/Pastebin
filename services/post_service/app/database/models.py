import uuid
from datetime import datetime
from typing import Annotated
from sqlalchemy import DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


# created_at = Annotated[datetime, mapped_column(
#     server_default=text("TIMEZONE('utc', now())"))]
# updated_at = Annotated[datetime, mapped_column(
#     server_default=text("TIMEZONE('utc', now())"),
#     onupdate=datetime.utcnow()
# )]


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(50), index=True)
    content: Mapped[str] = mapped_column(String(1024))

    author_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    )
