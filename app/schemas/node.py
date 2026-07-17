from __future__ import annotations

from pydantic import BaseModel


class NodeResponse(BaseModel):
    id: int
    title: str
    body: str | None
    level: int
    page_number: int
    content_hash: str
    children: list["NodeResponse"] = []

    model_config = {
        "from_attributes": True
    }


NodeResponse.model_rebuild()