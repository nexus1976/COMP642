import uuid
from typing import Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import * # type: ignore
from api.infrastructure.postgres.dbcontext import DBContext
from api.models.venue import Venue
from api.infrastructure.postgres.venues import Venue as VenueModel

class VenueRepository():
    def __init__(self, dbcontext: DBContext) -> None:
        self._dbcontext: DBContext = dbcontext

    model_class = VenueModel

    def _to_entity(self, model: VenueModel) -> Venue:
        venue = Venue(
            id=model.id,
            name=model.name, 
            address=model.address, 
            capacity=model.capacity
        )
        return venue

    def _to_model(self, entity: Venue) -> VenueModel:
        return VenueModel(
            id=entity.id,
            name=entity.name,
            address=entity.address,
            capacity=entity.capacity,
        )

    def add(self, venue: Venue) -> Venue: # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        entity = self._to_model(venue)
        session.add(entity)
        session.commit()
        session.close()
        return venue

    def update(self, venue: Venue) -> Optional[Venue]: # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        record = session.query(VenueModel).filter(VenueModel.id == venue.id).first()
        if not record:
            session.close()
            return None
        record.name = venue.name
        record.address = venue.address
        record.capacity = venue.capacity
        session.commit()
        session.close()
        return venue    

    def delete(self, id: uuid.UUID) -> None:
        session: Session = self._dbcontext.createSession()
        record = session.query(VenueModel).filter(VenueModel.id == id).first()
        if not record:
            session.close()
            return None
        session.delete(record)
        session.commit()
        session.close()
        return None        

    def getall(self) -> List[Venue]:
        response: List[Venue] = list()
        session: Session = self._dbcontext.createSession()
        query = select(VenueModel)
        records = session.execute(query).fetchall()
        for record in records:
            entity: Venue = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response

    def get_by_id(self, id: uuid.UUID) -> Optional[Venue]:
        response: List[Venue] = list()
        session: Session = self._dbcontext.createSession()
        record = session.query(VenueModel).filter(VenueModel.id == id).first()
        session.close()
        if not record:
            return None
        entity = self._to_entity(record)
        return entity  

    def search_by_name(self, name: str) -> List[Venue]:
        response: List[Venue] = list()
        session: Session = self._dbcontext.createSession()
        query = select(VenueModel).filter(VenueModel.name == name)
        records = session.execute(query).fetchall()
        for record in records:
            entity: Venue = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response

