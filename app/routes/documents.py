from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.models.node import Node
from app.schemas.change import NodeChangeResponse
from app.schemas.document import DocumentResponse
from app.schemas.node import NodeResponse
from app.services.versioning import VersioningService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def list_documents(
    db: Session = Depends(get_db),
):
    """
    Return all documents.
    """
    return db.query(Document).all()


@router.get("/search")
def search_nodes(
    q: str,
    db: Session = Depends(get_db),
):
    """
    Search node titles and body text.
    """

    nodes = (
        db.query(Node)
        .filter(
            or_(
                Node.title.ilike(f"%{q}%"),
                Node.body.ilike(f"%{q}%"),
            )
        )
        .all()
    )

    return [
        {
            "id": node.id,
            "title": node.title,
            "page_number": node.page_number,
            "level": node.level,
        }
        for node in nodes
    ]


@router.get(
    "/nodes/{node_id}",
    response_model=NodeResponse,
)
def get_node(
    node_id: int,
    db: Session = Depends(get_db),
):
    """
    Return a node with its children.
    """

    node = db.query(Node).filter(Node.id == node_id).first()

    if node is None:
        raise HTTPException(
            status_code=404,
            detail="Node not found",
        )

    return node


@router.get(
    "/nodes/{node_id}/changes",
    response_model=NodeChangeResponse,
)
def get_node_changes(
    node_id: int,
    db: Session = Depends(get_db),
):
    """
    Return whether a node changed compared to the previous version.
    """

    service = VersioningService()

    return service.node_changes(
        db=db,
        node_id=node_id,
    )