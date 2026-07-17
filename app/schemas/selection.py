from pydantic import BaseModel


class SelectionCreate(BaseModel):
    name: str
    node_ids: list[int]


class SelectionResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }