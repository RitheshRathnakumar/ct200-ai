from app.database import SessionLocal
from app.models.document import Document
from app.models.document_version import DocumentVersion
from app.models.node import Node

db = SessionLocal()

print("\nDocuments")
print("-" * 40)

for document in db.query(Document).all():
    print(document.id, document.title)

print("\nVersions")
print("-" * 40)

for version in db.query(DocumentVersion).all():
    print(version.id, version.version_number)

print("\nNodes")
print("-" * 40)

print("Total Nodes:", db.query(Node).count())

db.close()