from __future__ import annotations

from app.services.heading_detector import is_heading
from app.services.level_detector import detect_level
from app.services.types import DocumentNode, TextBlock


class HierarchyBuilder:
    """
    Reconstructs a hierarchical document tree from ordered TextBlocks.
    """

    def build(self, blocks: list[TextBlock]) -> list[DocumentNode]:

        root_nodes: list[DocumentNode] = []

        stack: list[DocumentNode] = []

        for block in blocks:

            if is_heading(block):
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

            else:

                if stack:
                    if stack[-1].body:
                        stack[-1].body += "\n"

                    stack[-1].body += block.text.strip()

        return root_nodes