from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from opsflow.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from opsflow.models.user import User


class Ticket(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN", index=True, nullable=False)
    priority: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    author: Mapped["User"] = relationship(lazy="joined")

class TicketCreate(Base):
    title: str
    description: str
    priority: str = "MEDIUM"

class TicketUpdateStatus(Base):
    status: str

class TicketRead(Base, TimestampMixin):
    id: int
    title: str
    description: str
    status: str
    priority: str 
    author_id: int
