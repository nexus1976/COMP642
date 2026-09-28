import uuid
from pydantic import BaseModel, Field

class User(BaseModel):
    id: uuid.UUID = Field(...)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)
    username: str = Field(..., min_length=8)
    isadmin: bool = Field(True)