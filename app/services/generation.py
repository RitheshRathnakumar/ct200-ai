from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from pymongo.collection import Collection
from sqlalchemy.orm import Session

from app.database_mongo import generations_collection
from app.models.node import Node
from app.models.selection import Selection
from app.models.selection_node import SelectionNode
from app.schemas.generation import GenerationResponse
from app.services.gemini_client import generate
from app.services.json_validator import (
    LLMValidationError,
    validate_llm_response,
)
from app.services.prompts import (
    PROMPT_VERSION,
    build_generation_prompt,
)


class GenerationService:
    """
    Handles QA test case generation from version-pinned selections.
    """

    def __init__(
        self,
        db: Session,
        mongo: Collection = generations_collection,
    ):
        self.db = db
        self.mongo = mongo

    # ----------------------------------------------------
    # Selection Loading
    # ----------------------------------------------------

    def _get_selection(
        self,
        selection_id: int,
    ) -> Selection:

        selection = self.db.get(
            Selection,
            selection_id,
        )

        if selection is None:
            raise ValueError(
                f"Selection {selection_id} not found."
            )

        return selection

    def _get_selection_nodes(
        self,
        selection: Selection,
    ) -> list[SelectionNode]:

        return (
            self.db.query(SelectionNode)
            .filter(
                SelectionNode.selection_id == selection.id
            )
            .all()
        )

    # ----------------------------------------------------
    # Document Reconstruction
    # ----------------------------------------------------

    def _build_document_text(
        self,
        nodes: list[SelectionNode],
    ) -> str:

        parts: list[str] = []

        for item in nodes:

            node: Node = item.node

            parts.append(
                f"# {node.title}\n\n"
                f"{node.body or ''}"
            )

        return "\n\n".join(parts)

    # ----------------------------------------------------
    # Hash Utilities
    # ----------------------------------------------------

    def _selection_hash(
        self,
        nodes: list[SelectionNode],
    ) -> str:

        digest = hashlib.sha256()

        for item in nodes:

            digest.update(
                item.node.content_hash.encode()
            )

        return digest.hexdigest()

    def _node_hashes(
        self,
        nodes: list[SelectionNode],
    ) -> list[str]:

        return [
            item.node.content_hash
            for item in nodes
        ]

    def _node_ids(
        self,
        nodes: list[SelectionNode],
    ) -> list[int]:

        return [
            item.node.id
            for item in nodes
        ]

    # ----------------------------------------------------
    # Duplicate Detection
    # ----------------------------------------------------

    def _find_existing_generation(
        self,
        selection_hash: str,
    ):

        return self.mongo.find_one(
            {
                "selection_hash": selection_hash,
                "prompt_version": PROMPT_VERSION,
            }
        )

    # ----------------------------------------------------
    # Prompt Construction
    # ----------------------------------------------------

    def _build_prompt(
        self,
        selection: Selection,
        nodes: list[SelectionNode],
    ) -> str:

        document_text = self._build_document_text(
            nodes
        )

        return build_generation_prompt(
            selection.name,
            document_text,
        )
    # ----------------------------------------------------
    # LLM Generation
    # ----------------------------------------------------

    def _generate_test_cases(
        self,
        prompt: str,
    ) -> dict:

        raw_response = generate(prompt)

        try:
            validated = validate_llm_response(
                raw_response
            )

        except LLMValidationError as exc:
            raise RuntimeError(
                f"LLM validation failed: {exc}"
            )

        return validated

    # ----------------------------------------------------
    # MongoDB Storage
    # ----------------------------------------------------

    def _store_generation(
        self,
        selection: Selection,
        nodes: list[SelectionNode],
        selection_hash: str,
        generation: dict,
    ) -> dict:

        document_version = nodes[0].version_id

        document = {
            "selection_id": selection.id,
            "selection_name": selection.name,
            "selection_hash": selection_hash,
            "document_version": document_version,
            "node_ids": self._node_ids(nodes),
            "node_hashes": self._node_hashes(nodes),
            "prompt_version": PROMPT_VERSION,
            "model": "gemini-flash-latest",
            "generated_at": datetime.now(timezone.utc),
            "test_cases": generation["test_cases"],
        }

        result = self.mongo.insert_one(document)

        document["_id"] = result.inserted_id

        return document
    # ----------------------------------------------------
    # Response Builder
    # ----------------------------------------------------

    def build_response(
        self,
        document: dict,
    ) -> GenerationResponse:
        """
        Convert a MongoDB document into a GenerationResponse.
        """

        return GenerationResponse(
            generation_id=str(document["_id"]),
            selection_id=document["selection_id"],
            selection_name=document["selection_name"],
            selection_hash=document["selection_hash"],
            document_version=document["document_version"],
            node_ids=document["node_ids"],
            node_hashes=document["node_hashes"],
            prompt_version=document["prompt_version"],
            model=document["model"],
            generated_at=document["generated_at"],
            cached=document.get("cached", False),
            test_cases=document["test_cases"],
        )
    # ----------------------------------------------------
    # Public API
    # ----------------------------------------------------

    def generate(
        self,
        selection_id: int,
    ) -> dict:

        selection = self._get_selection(
            selection_id
        )

        nodes = self._get_selection_nodes(
            selection
        )

        if not nodes:
            raise ValueError(
                "Selection contains no nodes."
            )

        selection_hash = self._selection_hash(
            nodes
        )

        existing = self._find_existing_generation(
            selection_hash
        )

        if existing is not None:


            existing["cached"] = True

            return existing

        prompt = self._build_prompt(
            selection,
            nodes,
        )

        generation = self._generate_test_cases(
            prompt
        )

        stored = self._store_generation(
            selection,
            nodes,
            selection_hash,
            generation,
        )

        stored["cached"] = False

        return stored