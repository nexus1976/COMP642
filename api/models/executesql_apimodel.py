import uuid
from pydantic import BaseModel, Field

class ExecuteSQLModel(BaseModel):
    sql: str = Field(..., min_length=1)