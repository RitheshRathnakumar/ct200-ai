from __future__ import annotations

import re

from app.services.types import TextBlock


LIST_PATTERN = re.compile(r"^\d+\.\s")


def classify_block(block: TextBlock) -> str:
    """
    Classify a text block based on formatting and content.
    """

    text = block.text.strip()

    # Document title
    if block.font_size >= 20:
        return "title"

    # Main heading
    if block.font_size >= 16:
        return "heading"

    # Numbered subsection
    if block.font_size >= 12 and re.match(r"^\d+(\.\d+)*", text):
        return "subheading"

    # Numbered list
    if LIST_PATTERN.match(text):
        return "list_item"

    # Measurement/specification lines
    if re.fullmatch(r"[0-9A-Za-z×x\-\–≥≤./ ()%]+", text):
        return "measurement"

    return "paragraph"