from __future__ import annotations

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.database_mongo import generations_collection
from app.schemas.generation import (
    GenerateRequest,
    GenerateResponse,
    RetrievalResponse,
)
from app.services.generation import GenerationService
from app.services.staleness import StalenessService

router = APIRouter(
    prefix="/generations",
    tags=["Generations"],
)


# ----------------------------------------------------
# Generate Test Cases
# ----------------------------------------------------


@router.post(
    "",
    response_model=GenerateResponse,
)
def generate_test_cases(
    request: GenerateRequest,
    db: Session = Depends(get_db),
):

    service = GenerationService(db)

    try:
        generation = service.generate(
            request.selection_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    return GenerateResponse(
        generation_id=str(generation["_id"]),
        cached=generation.get("cached", False),
    )


# ----------------------------------------------------
# Get Generation by Mongo ID
# ----------------------------------------------------


@router.get(
    "/{generation_id}",
    response_model=RetrievalResponse,
)
def get_generation(
    generation_id: str,
    db: Session = Depends(get_db),
):

    try:
        object_id = ObjectId(generation_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid generation id.",
        )

    document = generations_collection.find_one(
        {
            "_id": object_id,
        }
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Generation not found.",
        )

    service = GenerationService(db)

    staleness = StalenessService(db).check(
        node_ids=document["node_ids"],
        stored_hashes=document["node_hashes"],
    )

    return RetrievalResponse(
        generation=service.build_response(document),
        staleness=staleness,
    )


# ----------------------------------------------------
# Get Generations by Selection
# ----------------------------------------------------


@router.get(
    "/selection/{selection_id}",
    response_model=list[RetrievalResponse],
)
def get_by_selection(
    selection_id: int,
    db: Session = Depends(get_db),
):

    service = GenerationService(db)

    documents = list(
        generations_collection.find(
            {
                "selection_id": selection_id,
            }
        )
    )

    results: list[RetrievalResponse] = []

    for document in documents:

        staleness = StalenessService(db).check(
            node_ids=document["node_ids"],
            stored_hashes=document["node_hashes"],
        )

        results.append(
            RetrievalResponse(
                generation=service.build_response(
                    document
                ),
                staleness=staleness,
            )
        )

    return results


# ----------------------------------------------------
# Get Generations containing a Node
# ----------------------------------------------------


@router.get(
    "/node/{node_id}",
    response_model=list[RetrievalResponse],
)
def get_by_node(
    node_id: int,
    db: Session = Depends(get_db),
):

    service = GenerationService(db)

    documents = list(
        generations_collection.find(
            {
                "node_ids": node_id,
            }
        )
    )

    results: list[RetrievalResponse] = []

    for document in documents:

        staleness = StalenessService(db).check(
            node_ids=document["node_ids"],
            stored_hashes=document["node_hashes"],
        )

        results.append(
            RetrievalResponse(
                generation=service.build_response(
                    document
                ),
                staleness=staleness,
            )
        )

    return results


# ----------------------------------------------------
# List All Generations
# ----------------------------------------------------


@router.get("")
def list_generations():

    documents = list(
        generations_collection.find()
    )

    for document in documents:
        document["_id"] = str(document["_id"])

    return documents