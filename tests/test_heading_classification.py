from app.services.block_classifier import classify_block
from app.services.types import TextBlock


def make_block(text, font_size):
    return TextBlock(
        text=text,
        page_number=1,
        font_size=font_size,
        font_name="Helvetica-Bold",
        is_bold=True,
        flags=0,
        bbox=(0, 0, 100, 20),
    )


def test_title_classification():
    assert classify_block(make_block("CT-200", 22)) == "title"


def test_heading_classification():
    assert classify_block(make_block("Safety Information", 16)) == "heading"


def test_subheading_classification():
    assert classify_block(make_block("1.1 Battery Installation", 12)) == "subheading"