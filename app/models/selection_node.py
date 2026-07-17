from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.node import Node
    from app.models.document_version import DocumentVersion
    from app.models.selection import Selection


class SelectionNode(Base):
    """
    Stores the nodes belonging to a selection.
    Each record is pinned to a specific document version.
    """

    __tablename__ = "selection_nodes"

    id: Mapped[int] = mapped_column(primary_key=True)

    selection_id: Mapped[int] = mapped_column(
        ForeignKey("selections.id"),
        nullable=False,
    )

    node_id: Mapped[int] = mapped_column(
        ForeignKey("nodes.id"),
        nullable=False,
    )

    version_id: Mapped[int] = mapped_column(
        ForeignKey("document_versions.id"),
        nullable=False,
    )

    selection: Mapped["Selection"] = relationship(
        back_populates="nodes",
    )

    node: Mapped["Node"] = relationship()

    version: Mapped["DocumentVersion"] = relationship()