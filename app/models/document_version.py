from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.node import Node


class DocumentVersion(Base):
    """Represents a specific version of a document."""

    __tablename__ = "document_versions"

    id: Mapped[int] = mapped_column(primary_key=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
    )
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)

    # Link back to the parent document.
    document: Mapped["Document"] = relationship(back_populates="versions")

    # A document version can contain many nodes.
    nodes: Mapped[list["Node"]] = relationship(back_populates="document_version")
