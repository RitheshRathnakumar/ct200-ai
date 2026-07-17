from app.database import Base, SessionLocal, engine
from app.services.ingestion import IngestionService

# Create database tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    service = IngestionService()

    document = service.ingest(
        db=db,
        pdf_path="data/ct200_manual.pdf",
        title="CardioTrack CT-200 Manual",
    )

    print("=" * 50)
    print("Document ingested successfully!")
    print(f"Document ID      : {document.id}")
    print(f"Document Title   : {document.title}")
    print("=" * 50)

finally:
    db.close()