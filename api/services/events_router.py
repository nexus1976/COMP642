import uuid
import os
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, Query, status, Response
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.binary import Binary, UuidRepresentation
from api.infrastructure.postgres.dbcontext import DBContext
from api.models.event import Event
from api.models.review import Review
from api.models.event_repository import EventRepository

router = APIRouter(tags=["events"])

def find_event_content(query: Dict[str, Any]) -> List[Dict[str, Any]]:
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_username = os.getenv("MONGO_USERNAME", "dbuser")
    mongo_password = os.getenv("MONGO_PASSWORD", "password1234")

    try:
        with MongoClient(
            host=mongo_host,
            port=27017,
            username=mongo_username,
            password=mongo_password,
            authSource="admin",
            uuidRepresentation="standard",
            serverSelectionTimeoutMS=5000,
        ) as client:
            return list(
                client["group4db"]["event_content"].find(query, {"_id": 0})
            )
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to search event content.",
        ) from exc

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
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_username = os.getenv("MONGO_USERNAME", "dbuser")
    mongo_password = os.getenv("MONGO_PASSWORD", "password1234")

    try:
        with MongoClient(
            host=mongo_host,
            port=27017,
            username=mongo_username,
            password=mongo_password,
            authSource="admin",
            uuidRepresentation="standard",
            serverSelectionTimeoutMS=5000,
        ) as client:
            content = client["group4db"]["event_content"].find_one(
                {"eventId": Binary.from_uuid(id, UuidRepresentation.STANDARD)},
                {"_id": 0},
            )
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve event content.",
        ) from exc

    if content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event content not found.",
        )

    res.status_code = status.HTTP_200_OK
    return jsonable_encoder(content)

@router.post("/events/{id}/reviews", status_code=status.HTTP_201_CREATED | status.HTTP_404_NOT_FOUND | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def create_event_review(res: Response, id: uuid.UUID, payload: Review):
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_username = os.getenv("MONGO_USERNAME", "dbuser")
    mongo_password = os.getenv("MONGO_PASSWORD", "password1234")
    event_id = Binary.from_uuid(id, UuidRepresentation.STANDARD)
    review_document = {
        "reviewer": payload.reviewer,
        "rating": payload.rating,
        "comment": payload.comment,
    }

    try:
        with MongoClient(
            host=mongo_host,
            port=27017,
            username=mongo_username,
            password=mongo_password,
            authSource="admin",
            uuidRepresentation="standard",
            serverSelectionTimeoutMS=5000,
        ) as client:

            result = client["group4db"]["event_content"].update_one(
                {"eventId": event_id},
                {"$push": {"Reviews": review_document}},
            )
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save event review.",
        ) from exc

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event content not found.",
        )

    res.status_code = status.HTTP_201_CREATED
    return {
        "event_id": id,
        "review": payload,
    }

@router.delete("/events/{id}/reviews/{reviewer}", status_code=status.HTTP_200_OK | status.HTTP_404_NOT_FOUND | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def delete_event_reviews(res: Response, id: uuid.UUID, reviewer: str):
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_username = os.getenv("MONGO_USERNAME", "dbuser")
    mongo_password = os.getenv("MONGO_PASSWORD", "password1234")
    event_id = Binary.from_uuid(id, UuidRepresentation.STANDARD)

    try:
        with MongoClient(
            host=mongo_host,
            port=27017,
            username=mongo_username,
            password=mongo_password,
            authSource="admin",
            uuidRepresentation="standard",
            serverSelectionTimeoutMS=5000,
        ) as client:
            event_content = client["group4db"]["event_content"]
            event_document = event_content.find_one(
                {"eventId": event_id},
                {"Reviews": 1},
            )
            if event_document is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Event content not found.",
                )

            deleted_reviews = sum(
                1
                for review in event_document.get("Reviews", [])
                if review.get("reviewer") == reviewer
            )
            event_content.update_one(
                {"eventId": event_id},
                {"$pull": {"Reviews": {"reviewer": reviewer}}},
            )
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete event reviews.",
        ) from exc

    res.status_code = status.HTTP_200_OK
    return {
        "event_id": id,
        "reviewer": reviewer,
        "deleted_reviews": deleted_reviews,
    }

@router.get("/events/search/tags/{tag}")
async def find_events_by_tag(tag: str):
    documents = find_event_content({"Tags": tag})
    return jsonable_encoder(documents)

@router.get("/events/search/speakers/{speaker}")
async def find_events_by_speaker(speaker: str):
    documents = find_event_content({"Speakers.name": speaker})
    return jsonable_encoder(documents)

@router.get("/events/search/reviews")
async def find_events_by_review_rating(
    rating: int = Query(..., ge=1, le=5, description="Return events with a review above this rating."),
):
    documents = find_event_content({
        "Reviews": {
            "$elemMatch": {
                "rating": {"$gte": rating},
            }
        }
    })
    return jsonable_encoder(documents)

@router.get("/events/search/attributes")
async def find_events_by_nested_attributes(
    speaker_role: str | None = None,
    speaker_topic: str | None = None,
    min_review_rating: int | None = Query(None, ge=1, le=5),
    age_restriction: str | None = None,
    tag: str | None = None,
):
    conditions: List[Dict[str, Any]] = []

    speaker_attributes = {
        key: value
        for key, value in {
            "role": speaker_role,
            "topic": speaker_topic,
        }.items()
        if value is not None
    }
    if speaker_attributes:
        conditions.append({"Speakers": {"$elemMatch": speaker_attributes}})
    if min_review_rating is not None:
        conditions.append({
            "Reviews": {
                "$elemMatch": {"rating": {"$gte": min_review_rating}}
            }
        })
    if age_restriction is not None:
        conditions.append({"Description.ageRestriction": age_restriction})
    if tag is not None:
        conditions.append({"Tags": tag})

    if not conditions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one nested attribute to search for.",
        )

    documents = find_event_content({"$and": conditions})
    return jsonable_encoder(documents)

@router.get("/events/search/concerts/genre/{genre}")
async def find_concerts_by_genre(genre: str):
    documents = find_event_content({
        "$and": [
            {"Tags": "concert"},
            {"$or": [{"Genre": genre}, {"Tags": genre}]},
        ]
    })
    return jsonable_encoder(documents)

@router.get("/trending")
async def get_trending_events():
    # Replace with Redis-backed trending list later
    return {
        "items": [
            {"event_id": "evt_123", "score": 98},
            {"event_id": "evt_456", "score": 86}
        ]
    }