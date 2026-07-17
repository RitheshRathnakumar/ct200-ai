from app.services.hierarchy import HierarchyBuilder
from app.services.types import TextBlock


def block(text, size):
    return TextBlock(
        text=text,
        page_number=1,
        font_size=size,
        font_name="Helvetica",
        is_bold=size >= 12,
        flags=0,
        bbox=(0, 0, 100, 20),
    )


def test_duplicate_headings_create_two_nodes():
    builder = HierarchyBuilder()

    tree = builder.build(
        [
            block("Warnings", 16),
            block("First warning", 11),
            block("Warnings", 16),
            block("Second warning", 11),
        ]
    )

    assert len(tree) == 2
    assert tree[0].title == "Warnings"
    assert tree[1].title == "Warnings"
    assert tree[0].body == "First warning"
    assert tree[1].body == "Second warning"