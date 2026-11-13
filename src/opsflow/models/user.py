from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from opsflow.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="EMPLOYEE", nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
