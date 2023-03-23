import enum
from typing import Optional, List

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base
import src.constants.user as constants


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
    note: Mapped[List["Note"]] = relationship("User", back_populates="user")
