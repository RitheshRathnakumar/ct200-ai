from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TextBlock:
    """
    Represents one logical text block extracted from the PDF.
    """

    text: str
    page_number: int

    font_size: float
    font_name: str

    is_bold: bool
    flags: int

    bbox: tuple[float, float, float, float]

    block_type: str = "paragraph"

    level: int = 0

    is_heading: bool = False


@dataclass
class DocumentNode:
    """
    Represents one node in the reconstructed document tree.
    """

    title: str
    level: int
    page_number: int

    body: str = ""

    children: list["DocumentNode"] = field(default_factory=list)