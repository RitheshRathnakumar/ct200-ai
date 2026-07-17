from __future__ import annotations

import hashlib


def generate_content_hash(text: str) -> str:
    """
    Generate a stable SHA-256 hash for a string.
    """

    normalized = " ".join(text.split())

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


def hash_node(title: str, body: str) -> str:
    """
    Generate a stable hash for an entire document node.
    """

    return generate_content_hash(
        title.strip() + "\n" + body.strip()
    )