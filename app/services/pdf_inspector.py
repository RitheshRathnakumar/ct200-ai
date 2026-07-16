from __future__ import annotations

from collections import Counter
from pathlib import Path

import fitz


def inspect_pdf(pdf_path: str) -> None:
    """
    Inspect a PDF and print information useful for designing
    the document parser.

    Reports:
    - Page count
    - Font sizes
    - Font names
    - Bold flags
    - Text block previews
    """

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    with fitz.open(pdf_path) as doc:
        print("=" * 80)
        print(f"PDF: {pdf_file.name}")
        print(f"Pages: {len(doc)}")
        print("=" * 80)

        font_sizes = Counter()

        for page_number, page in enumerate(doc, start=1):

            print(f"\nPAGE {page_number}")
            print("-" * 80)

            data = page.get_text("dict")

            for block in data["blocks"]:

                if "lines" not in block:
                    continue

                for line in block["lines"]:

                    line_text = ""

                    for span in line["spans"]:

                        size = round(span["size"], 1)
                        font = span["font"]
                        flags = span["flags"]

                        font_sizes[size] += 1

                        line_text += span["text"]

                        print(
                            f"Font={font:25}"
                            f" Size={size:<5}"
                            f" Flags={flags:<3}"
                            f" Text={span['text'][:80]}"
                        )

                    if line_text.strip():
                        print(f"  → {line_text}")

        print("\n")
        print("=" * 80)
        print("FONT SIZE SUMMARY")
        print("=" * 80)

        for size, count in sorted(font_sizes.items()):
            print(f"{size:>5} pt : {count} spans")