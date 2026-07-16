from __future__ import annotations

import re

from app.services.types import TextBlock


NUMBER_PATTERN = re.compile(r"^(\d+(?:\.\d+)*)")


def detect_level(block: TextBlock) -> int:
    """
    Determine the hierarchy level of a heading.

    Examples:
        1           -> 1
        1.2         -> 2
        1.2.3       -> 3
        1.2.3.4     -> 4

    Non-numbered headings default to level 1.
    """

    match = NUMBER_PATTERN.match(block.text.strip())

    if not match:
        return 1

    numbering = match.group(1)

    return numbering.count(".") + 1