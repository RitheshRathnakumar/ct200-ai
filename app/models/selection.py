from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.selection_node import SelectionNode


class Selection(Base):
    """
    Represents a named collection of document nodes.
    """

    __tablename__ = "selections"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
    )

    nodes: Mapped[list["SelectionNode"]] = relationship(
        back_populates="selection",
        cascade="all, delete-orphan",
    )