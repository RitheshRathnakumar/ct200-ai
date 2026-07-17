from app.database import SessionLocal
from app.services.versioning import VersioningService

db = SessionLocal()

try:
    service = VersioningService()

    # Change this ID to any node that exists
    node_id = 32

    result = service.node_changes(
        db=db,
        node_id=node_id,
    )

    print("=" * 60)
    print(f"Node ID: {node_id}")
    print("=" * 60)

    for key, value in result.items():
        print(f"{key}:")
        print(value)
        print()

finally:
    db.close()