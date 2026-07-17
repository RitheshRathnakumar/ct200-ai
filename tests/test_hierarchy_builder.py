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


def test_parent_child_relationship():
    builder = HierarchyBuilder()

    tree = builder.build(
        [
            block("Safety", 16),
            block("1.1 General", 12),
            block("Read the manual.", 11),
        ]
    )

    assert len(tree) == 1
    assert len(tree[0].children) == 1
    assert tree[0].children[0].title == "1.1 General"
    assert tree[0].children[0].body == "Read the manual."