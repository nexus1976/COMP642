import uuid
import os
from typing import List
from fastapi import APIRouter, HTTPException, status, Response
from api.infrastructure.postgres.dbcontext import DBContext
from api.models.event import Event
from api.models.review import Review
from api.models.event_repository import EventRepository

router = APIRouter(tags=["events"])

@router.get("/events", status_code=status.HTTP_200_OK | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def list_events(res: Response) -> List[Event]:
    dbcontext: DBContext = DBContext(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], username=os.environ['DB_UID'], password=os.environ['DB_PWD'])
    eventRepo: EventRepository = EventRepository(dbcontext=dbcontext)
    response = eventRepo.getall()
    res.status_code = status.HTTP_200_OK
    return response

@router.get("/events/{id}", status_code=status.HTTP_200_OK | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def get_event(res: Response, id: uuid.UUID) -> Event | None:
    dbcontext: DBContext = DBContext(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], username=os.environ['DB_UID'], password=os.environ['DB_PWD'])
    eventRepo: EventRepository = EventRepository(dbcontext=dbcontext)
    response = eventRepo.get_by_id(id)
    res.status_code = status.HTTP_200_OK
    return response   

@router.get("/events/{id}/content")
async def get_event_content(res: Response, id: uuid.UUID):
    # Replace with MongoDB content document later
    return {
        "event_id": id,
        "content": {
            "description": "Event description and rich content",
            "highlights": ["Keynote", "Networking", "VIP access"],
            "schedule": []
        }
    }

@router.post("/events/{id}/reviews", status_code=status.HTTP_201_CREATED | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def create_event_review(id: uuid.UUID, payload: Review):
    # Replace with MongoDB review insert + Postgres event validation later
    return {
        "event_id": id,
        "review": {
            "user_id": payload.user_id,
            "rating": payload.rating,
            "comment": payload.comment
        }
    }

@router.get("/trending")
async def get_trending_events():
    # Replace with Redis-backed trending list later
    return {
        "items": [
            {"event_id": "evt_123", "score": 98},
            {"event_id": "evt_456", "score": 86}
        ]
    }