from app.database import SessionLocal
from app.models.document_version import DocumentVersion
from app.services.versioning import VersioningService

db = SessionLocal()

try:
    print("=" * 60)
    print("Available Versions")
    print("=" * 60)

    versions = db.query(DocumentVersion).all()

    for version in versions:
        print(
            f"ID={version.id}  "
            f"Document={version.document_id}  "
            f"Version={version.version_number}"
        )

    print("\nComparing Version 1 and Version 2...\n")

    service = VersioningService()

    changes = service.compare_versions(
        db=db,
        document_id=1,
        old_version=1,
        new_version=2,
    )

    if not changes:
        print("✅ No changes detected.")

    else:
        print("Changes detected:")
        for change in changes:
            print(change)

finally:
    db.close()