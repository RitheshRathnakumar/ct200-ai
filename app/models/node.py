from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.document_version import DocumentVersion


class Node(Base):
    """Represents a node within a document version."""

    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    level: Mapped[int] = mapped_column(nullable=False)
    page_number: Mapped[int] = mapped_column(nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    document_version_id: Mapped[int] = mapped_column(
        ForeignKey("document_versions.id"),
        nullable=False,
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("nodes.id"),
        nullable=True,
    )

    # Link to the owning document version.
    document_version: Mapped["DocumentVersion"] = relationship(back_populates="nodes")

    # Self-referencing parent/child hierarchy.
    parent: Mapped["Node | None"] = relationship(back_populates="children", remote_side="Node.id")
    children: Mapped[list["Node"]] = relationship(back_populates="parent")
