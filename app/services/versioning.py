from __future__ import annotations

from difflib import unified_diff

from sqlalchemy.orm import Session

from app.models.document_version import DocumentVersion
from app.models.node import Node


class VersioningService:
    """
    Compare document versions and detect node changes.
    """

    def compare_versions(
        self,
        db: Session,
        document_id: int,
        old_version: int,
        new_version: int,
    ) -> list[dict]:

        old = (
            db.query(DocumentVersion)
            .filter(
                DocumentVersion.document_id == document_id,
                DocumentVersion.version_number == old_version,
            )
            .first()
        )

        new = (
            db.query(DocumentVersion)
            .filter(
                DocumentVersion.document_id == document_id,
                DocumentVersion.version_number == new_version,
            )
            .first()
        )

        if old is None or new is None:
            return []

        old_nodes = (
            db.query(Node)
            .filter(Node.document_version_id == old.id)
            .all()
        )

        new_nodes = (
            db.query(Node)
            .filter(Node.document_version_id == new.id)
            .all()
        )

        old_map = {
            node.title: node
            for node in old_nodes
        }

        changes = []

        for node in new_nodes:

            previous = old_map.get(node.title)

            if previous is None:
                changes.append(
                    {
                        "title": node.title,
                        "status": "NEW",
                    }
                )

            elif previous.content_hash != node.content_hash:
                changes.append(
                    {
                        "title": node.title,
                        "status": "MODIFIED",
                    }
                )

        return changes

    def node_changes(
        self,
        db: Session,
        node_id: int,
    ) -> dict:
        """
        Return change information for a single node compared
        with the previous document version.
        """

        node = db.get(Node, node_id)

        if node is None:
            return {
                "changed": False,
                "summary": "Node not found."
            }

        version = db.get(
            DocumentVersion,
            node.document_version_id,
        )

        if version.version_number == 1:
            return {
                "changed": False,
                "summary": "First version of the document."
            }

        previous_version = (
            db.query(DocumentVersion)
            .filter(
                DocumentVersion.document_id == version.document_id,
                DocumentVersion.version_number == version.version_number - 1,
            )
            .first()
        )

        previous_node = (
            db.query(Node)
            .filter(
                Node.document_version_id == previous_version.id,
                Node.title == node.title,
            )
            .first()
        )

        if previous_node is None:
            return {
                "changed": True,
                "summary": "New node."
            }

        if previous_node.content_hash == node.content_hash:
            return {
                "changed": False,
                "summary": "No changes detected."
            }

        diff = "\n".join(
            unified_diff(
                (previous_node.body or "").splitlines(),
                (node.body or "").splitlines(),
                lineterm="",
            )
        )

        return {
            "changed": True,
            "old_hash": previous_node.content_hash,
            "new_hash": node.content_hash,
            "summary": diff[:500],
        }