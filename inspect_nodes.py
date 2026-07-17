from app.database import SessionLocal
import app.models

from app.models.node import Node

db = SessionLocal()

for node in db.query(Node).limit(5).all():
    print("=" * 50)
    print("ID:", node.id)
    print("Title:", node.title)
    print("Level:", node.level)
    print("Parent:", node.parent_id)
    print("Hash:", node.content_hash)
    print("Body length:", len(node.body or ""))

db.close()