from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.node import Node
from app.models.selection import Selection
from app.models.selection_node import SelectionNode
from app.schemas.selection import (
    SelectionCreate,
    SelectionResponse,
)

router = APIRouter(
    prefix="/selections",
    tags=["Selections"],
)


@router.post(
    "",
    response_model=SelectionResponse,
)
def create_selection(
    request: SelectionCreate,
    db: Session = Depends(get_db),
):
    """
    Create a version-pinned selection.
    """

    selection = Selection(name=request.name)

    db.add(selection)
    db.flush()

    for node_id in request.node_ids:

        node = db.get(Node, node_id)

        if node is None:
            raise HTTPException(
                status_code=404,
                detail=f"Node {node_id} not found.",
            )

        db.add(
            SelectionNode(
                selection_id=selection.id,
                node_id=node.id,
                version_id=node.document_version_id,
            )
        )

    db.commit()
    db.refresh(selection)

    return selection


@router.get(
    "",
    response_model=list[SelectionResponse],
)
def list_selections(
    db: Session = Depends(get_db),
):
    """
    Return all saved selections.
    """

    return db.query(Selection).all()