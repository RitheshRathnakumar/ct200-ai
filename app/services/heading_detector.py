from __future__ import annotations

import re

from app.services.types import TextBlock

HEADING_PATTERN = re.compile(r"^\d+(\.\d+)*")
LIST_ITEM_PATTERN = re.compile(r"^\d+\.\s")


def heading_score(block: TextBlock) -> int:
    """
    Calculate a confidence score that a text block is a heading.
    """

    score = 0
    text = block.text.strip()

    # Large fonts
    if block.font_size >= 16:
        score += 3
    elif block.font_size >= 13:
        score += 2

    # Bold text
    if block.is_bold:
        score += 2

    # Numbered headings (1, 1.2, 1.2.3)
    if HEADING_PATTERN.match(text):
        score += 3

    # Short text
    if len(text) < 80:
        score += 1

    # Headings usually don't end with a period
    if not text.endswith("."):
        score += 1

    # -------------------------
    # Reject common false positives
    # -------------------------

    # Measurement/value lines
    if re.fullmatch(r"[0-9A-Za-z×x\-\–≥≤./ ()%]+", text):
        score -= 5

    # Numbered list items like:
    # 1. Normal:
    # 2. Elevated:
    if LIST_ITEM_PATTERN.match(text) and ":" in text:
        score -= 5

    return score


def is_heading(block: TextBlock) -> bool:
    """
    Return True if the block is classified as a heading.
    """
    return heading_score(block) >= 5