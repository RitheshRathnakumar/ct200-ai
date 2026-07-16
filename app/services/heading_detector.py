import re

from app.services.types import TextBlock


HEADING_PATTERN = re.compile(r"^\d+(\.\d+)*")


def heading_score(block: TextBlock) -> int:
    """
    Calculate a confidence score that a text block is a heading.
    """

    score = 0

    text = block.text.strip()

    # Large fonts are usually headings
    if block.font_size >= 16:
        score += 3
    elif block.font_size >= 13:
        score += 2

    # Bold text is often a heading
    if block.is_bold:
        score += 2

    # Numbered headings like 1, 1.2, 3.4.5
    if HEADING_PATTERN.match(text):
        score += 3

    # Short text is more likely to be a heading
    if len(text) < 80:
        score += 1

    # Headings rarely end with a period
    if not text.endswith("."):
        score += 1

    return score


def is_heading(block: TextBlock) -> bool:
    """
    Return True if the block is classified as a heading.
    """

    return heading_score(block) >= 5