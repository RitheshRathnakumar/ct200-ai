from pydantic import BaseModel


class NodeChangeResponse(BaseModel):
    changed: bool
    summary: str
    old_hash: str | None = None
    new_hash: str | None = None