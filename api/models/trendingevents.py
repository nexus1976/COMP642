import uuid
from pydantic import BaseModel, Field

class TrendingEvents(BaseModel):
    event_id: uuid.UUID = Field(...)
    score: int = Field(0)

    def __init__(self, event_id: uuid.UUID, score: int):
        self.event_id = event_id
        self.score = score

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "score": self.score
        }