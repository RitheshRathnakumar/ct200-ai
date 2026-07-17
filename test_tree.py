from app.services.parser import PDFParser


def print_tree(nodes, indent=0):
    for node in nodes:
        print("  " * indent + f"- {node.title}")

        if node.body:
            print("  " * (indent + 1) + f"[Body: {len(node.body)} chars]")

        print_tree(node.children, indent + 1)


parser = PDFParser()

tree = parser.parse("data/ct200_manual.pdf")

print_tree(tree)