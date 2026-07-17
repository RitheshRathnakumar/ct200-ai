from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.node import Node


class StalenessService:
    """
    Determines whether a stored generation is still valid
    against the latest document contents.
    """

    def __init__(self, db: Session):
        self.db = db

    def check(
        self,
        node_ids: list[int],
        stored_hashes: list[str],
    ) -> dict:

        changed_nodes: list[int] = []

        for node_id, stored_hash in zip(
            node_ids,
            stored_hashes,
        ):

            node = self.db.get(
                Node,
                node_id,
            )

            if node is None:

                changed_nodes.append(node_id)
                continue

            if node.content_hash != stored_hash:

                changed_nodes.append(node_id)

        if changed_nodes:

            return {
                "status": "STALE",
                "changed_nodes": changed_nodes,
                "summary": (
                    f"{len(changed_nodes)} selected "
                    "section(s) changed."
                ),
            }

        return {
            "status": "CURRENT",
            "changed_nodes": [],
            "summary": "Generation is up to date.",
        }