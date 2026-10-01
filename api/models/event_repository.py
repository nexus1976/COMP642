import uuid
import datetime
from decimal import Decimal
from typing import Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import * # type: ignore
from api.infrastructure.postgres.dbcontext import DBContext
from api.models.event import Event
from api.infrastructure.postgres.events import Event as EventModel

class EventRepository:
    def __init__(self, dbcontext: DBContext) -> None:
        self._dbcontext: DBContext = dbcontext

    def _to_entity(self, model: EventModel) -> Event:
        event = Event(
            id=model.id,
            name=model.name,
            description=model.description,
            date=model.date,
            venue_id=model.venue_id,
            price=float(model.price)
        )
        return event

    def _to_model(self, entity: Event) -> EventModel:
        return EventModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            date=entity.date,
            venue_id=entity.venue_id,
            price=Decimal(str(entity.price)),
        )

    def add(self, event: Event) -> Event:  # type: ignore[override]
         session: Session = self._dbcontext.createSession()
         entity = self._to_model(event)
         session.add(entity)
         session.commit()
         session.close()
         return event

    def update(self, event: Event) -> Optional[Event]:  # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        record = session.query(EventModel).filter(EventModel.id == event.id).first()
        if not record:
            session.close()
            return None
        record.name = event.name
        record.description = event.description
        record.date = event.date
        record.venue_id = event.venue_id
        record.price = Decimal(event.price)
        session.commit()
        session.close()
        return event   

    def delete(self, id: uuid.UUID) -> None:
        session: Session = self._dbcontext.createSession()
        record = session.query(EventModel).filter(EventModel.id == id).first()
        if not record:
            session.close()
            return None
        session.delete(record)
        session.commit()
        session.close()
        return None 

    def getall(self) -> List[Event]:
        response: List[Event] = list()
        session: Session = self._dbcontext.createSession()
        query = select(EventModel)
        records = session.execute(query).fetchall()
        for record in records:
            entity: Event = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response

    def get_by_id(self, id: uuid.UUID) -> Optional[Event]:
        session: Session = self._dbcontext.createSession()
        record = session.query(EventModel).filter(EventModel.id == id).first()
        session.close()       
        if not record:
            return None
        entity = self._to_entity(record)
        return entity