from pydantic import BaseModel


class DocumentResponse(BaseModel):
    """
    Response model for a document.
    """

    id: int
    title: str

    model_config = {
        "from_attributes": True
    }