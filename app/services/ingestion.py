from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_version import DocumentVersion
from app.models.node import Node
from app.services.hashing import hash_node
from app.services.parser import PDFParser
from app.services.types import DocumentNode


class IngestionService:
    """
    Parses a PDF and stores its document tree in the database.
    Creates a new version if the document already exists.
    """

    def __init__(self):
        self.parser = PDFParser()

    def ingest(
        self,
        db: Session,
        pdf_path: str,
        title: str,
    ) -> Document:

        # Parse the PDF into a hierarchy
        tree = self.parser.parse(pdf_path)

        # Check if this document already exists
        document = (
            db.query(Document)
            .filter(Document.title == title)
            .first()
        )

        # Create the document if it doesn't exist
        if document is None:
            document = Document(title=title)
            db.add(document)
            db.flush()

        # Find the latest version
        latest_version = (
            db.query(DocumentVersion)
            .filter(DocumentVersion.document_id == document.id)
            .order_by(DocumentVersion.version_number.desc())
            .first()
        )

        next_version = 1

        if latest_version:
            next_version = latest_version.version_number + 1

        # Create a new version
        version = DocumentVersion(
            version_number=next_version,
            document_id=document.id,
        )

        db.add(version)
        db.flush()

        # Save all nodes recursively
        for node in tree:
            self._save_node(
                db=db,
                version_id=version.id,
                node=node,
                parent_id=None,
            )

        db.commit()

        return document

    def _save_node(
        self,
        db: Session,
        version_id: int,
        node: DocumentNode,
        parent_id: int | None,
    ) -> None:

        db_node = Node(
            title=node.title,
            body=node.body,
            level=node.level,
            page_number=node.page_number,
            parent_id=parent_id,
            document_version_id=version_id,
            content_hash=hash_node(
                node.title,
                node.body,
            ),
        )

        db.add(db_node)
        db.flush()

        for child in node.children:
            self._save_node(
                db=db,
                version_id=version_id,
                node=child,
                parent_id=db_node.id,
            )