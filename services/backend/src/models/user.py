import enum
from typing import Optional, List

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base
import constants.user as constants


class Status(enum.Enum):
    MALE = "m"
    FEMALE = "f"


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(constants.EMAIL_MAX_LENGTH),
        primary_key=True)
    hashed_password: Mapped[str] = mapped_column(
        String(constants.HASHED_PASSWORD_LENGTH)
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        String(constants.FIRSTNAME_MAX_LEGTH)
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(constants.LASTNAME_MAX_LEGTH)
    )
    sex: Mapped[Optional[Status]] = mapped_column(
        String(constants.SEX_LENGTH)
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        insert_default=True)
    note: Mapped[List["Note"]] = relationship(  # type: ignore
        "Note",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )
