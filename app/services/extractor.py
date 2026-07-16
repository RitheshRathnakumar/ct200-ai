from __future__ import annotations

from pathlib import Path

import fitz

from app.services.types import TextBlock


def extract_pages(pdf_path: str) -> list[TextBlock]:
    """
    Extract rich text blocks from a PDF.

    Each returned TextBlock preserves font metadata,
    making hierarchy reconstruction easier.
    """

    pdf = Path(pdf_path)

    if not pdf.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    blocks: list[TextBlock] = []

    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):

            page_dict = page.get_text("dict")

            for block in page_dict["blocks"]:

                # Skip image blocks
                if "lines" not in block:
                    continue

                for line in block["lines"]:

                    line_text = ""
                    font_size = 0.0
                    font_name = ""
                    flags = 0

                    for span in line["spans"]:

                        line_text += span["text"]

                        # Keep the largest font size in the line
                        font_size = max(font_size, span["size"])

                        # Preserve the first span's formatting
                        if not font_name:
                            font_name = span["font"]
                            flags = span["flags"]

                    if not line_text.strip():
                        continue

                    is_bold = (
                        "Bold" in font_name
                        or "bold" in font_name
                        or (flags & 16) != 0
                    )

                    blocks.append(
                        TextBlock(
                            text=line_text.strip(),
                            page_number=page_number,
                            font_size=font_size,
                            font_name=font_name,
                            is_bold=is_bold,
                            flags=flags,
                            bbox=tuple(block["bbox"]),
                        )
                    )

    return blocks
