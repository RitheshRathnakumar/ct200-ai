from __future__ import annotations

from app.services.extractor import extract_pages


class PDFParser:
    """
    High-level orchestration for the document ingestion pipeline.
    """

    def parse(self, pdf_path: str):

        pages = extract_pages(pdf_path)

        print(f"Extracted {len(pages)} pages.")

        return pages