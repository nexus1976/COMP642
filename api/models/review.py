import uuid
from pydantic import BaseModel, Field

class Review(BaseModel):
    id: uuid.UUID = Field(...)
    user_id: uuid.UUID = Field(...)
    rating: int = Field(1)
    comment: str = Field(..., min_length=1)