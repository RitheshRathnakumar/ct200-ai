from __future__ import annotations

from typing import Any

import fitz


def extract_pages(pdf_path: str) -> list[dict[str, Any]]:
    """
    Extract text from a PDF page by page.

    Returns:
        A list of dictionaries containing:
        - page_number
        - text
        - char_count
        - has_text
    """

    try:
        pages: list[dict[str, Any]] = []

        with fitz.open(pdf_path) as doc:
            for page_number, page in enumerate(doc, start=1):
                text = page.get_text()

                pages.append(
                    {
                        "page_number": page_number,
                        "text": text,
                        "char_count": len(text),
                        "has_text": bool(text.strip()),
                    }
                )

        return pages

    except Exception as exc:
        raise ValueError(f"Unable to open PDF: {pdf_path}") from exc
