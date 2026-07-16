from app.services.extractor import extract_pages
from app.services.heading_detector import is_heading
from app.services.level_detector import detect_level

blocks = extract_pages("data/ct200_manual.pdf")

print(f"Extracted {len(blocks)} text blocks\n")

for block in blocks:
    if is_heading(block):
        level = detect_level(block)
        print(f"[L{level}] {block.text}")