from __future__ import annotations

from app.services.extractor import extract_pages
from app.services.hierarchy import HierarchyBuilder


class PDFParser:
    """
    High-level orchestration for the document ingestion pipeline.
    """

    def __init__(self):
        self.builder = HierarchyBuilder()

    def parse(self, pdf_path: str):

        blocks = extract_pages(pdf_path)

        tree = self.builder.build(blocks)

        return tree