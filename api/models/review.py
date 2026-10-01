import uuid
from pydantic import BaseModel, Field

class Review(BaseModel):
    reviewer: str = Field(..., min_length=1)
    rating: int = Field(1)
    comment: str = Field(..., min_length=1)