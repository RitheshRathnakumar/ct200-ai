from __future__ import annotations

import hashlib


def generate_content_hash(text: str) -> str:
    """
    Generate a stable SHA-256 hash for a block of text.
    """

    normalized = " ".join(text.split())

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()