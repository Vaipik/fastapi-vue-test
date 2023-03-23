from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import UUID, DateTime

from src.db.base_class import Base
import src.constants.note as constants

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        insert_default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(constants.TITLE_MAX_LENGTH)
    )
    content: Mapped[str] = mapped_column(
        String(constants.CONTENT_MAX_LENGTH)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=datetime.utcnow
    )
    edited_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, onupdate=datetime.utcnow
    )
    user: Mapped["User"] = relationship("User", back_populates="note")
