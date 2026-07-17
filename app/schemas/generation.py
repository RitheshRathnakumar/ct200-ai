from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# ----------------------------------------------------
# Individual Test Case
# ----------------------------------------------------


class TestCase(BaseModel):
    title: str
    objective: str
    steps: list[str]
    expected_result: str
    traceability: list[str]


# ----------------------------------------------------
# Generate Request
# ----------------------------------------------------


class GenerateRequest(BaseModel):
    selection_id: int = Field(
        ...,
        gt=0,
        description="Selection to generate QA test cases from.",
    )


# ----------------------------------------------------
# Generate Response
# ----------------------------------------------------


class GenerateResponse(BaseModel):
    generation_id: str
    cached: bool


# ----------------------------------------------------
# Stored Generation
# ----------------------------------------------------


class GenerationResponse(BaseModel):
    generation_id: str

    selection_id: int

    selection_name: str

    selection_hash: str

    document_version: int

    node_ids: list[int]

    node_hashes: list[str]

    prompt_version: int

    model: str

    generated_at: datetime

    cached: bool = False

    test_cases: list[TestCase]


# ----------------------------------------------------
# Staleness
# ----------------------------------------------------


class StalenessResponse(BaseModel):
    status: Literal["CURRENT", "STALE"]

    changed_nodes: list[int]

    summary: str


# ----------------------------------------------------
# Retrieval Response
# ----------------------------------------------------


class RetrievalResponse(BaseModel):
    generation: GenerationResponse

    staleness: StalenessResponse