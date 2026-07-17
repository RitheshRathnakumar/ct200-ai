from __future__ import annotations

from app.services.block_classifier import classify_block
from app.services.level_detector import detect_level
from app.services.types import DocumentNode, TextBlock


class HierarchyBuilder:
    """
    Reconstruct a hierarchical document tree from TextBlocks.
    """

    def build(self, blocks: list[TextBlock]) -> list[DocumentNode]:

        root_nodes: list[DocumentNode] = []
        stack: list[DocumentNode] = []

        for block in blocks:

            block.block_type = classify_block(block)

            if block.block_type in ("title", "heading", "subheading"):

                block.level = detect_level(block)

                node = DocumentNode(
                    title=block.text.strip(),
                    level=block.level,
                    page_number=block.page_number,
                )

                while stack and stack[-1].level >= node.level:
                    stack.pop()

                if stack:
                    stack[-1].children.append(node)
                else:
                    root_nodes.append(node)

                stack.append(node)

            elif stack:
                if stack[-1].body:
                    stack[-1].body += "\n"

                stack[-1].body += block.text.strip()

        return root_nodes