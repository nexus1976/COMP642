import uuid
from decimal import Decimal
from typing import Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import * # type: ignore
from models.tickettype import TicketType
from api.infrastructure.postgres.tickettypes import TicketType as TicketTypeModel
from api.infrastructure.postgres.dbcontext import DBContext

class TicketTypeRepository():
    def __init__(self, dbcontext: DBContext) -> None:
        self._dbcontext: DBContext = dbcontext

    model_class = TicketTypeModel

    def _to_entity(self, model: TicketTypeModel) -> TicketType:
        ticket_type = TicketType(
            id=model.id,
            name=model.name,
            description=model.description,
            price=float(model.price)
        )
        return ticket_type

    def _to_model(self, entity: TicketType) -> TicketTypeModel:
        return TicketTypeModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            price=entity.price,
        )

    def add(self, ticketType: TicketType) -> TicketType:  # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        entity = self._to_model(ticketType)
        session.add(entity)
        session.commit()
        session.close()
        return ticketType

    def update(self, ticketType: TicketType) -> Optional[TicketType]:  # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        record = session.query(TicketTypeModel).filter(TicketTypeModel.id == ticketType.id).first()
        if not record:
            session.close()
            return None
        record.description = ticketType.description
        record.name = ticketType.name
        record.price = Decimal(ticketType.price)
        session.commit()
        session.close()
        return ticketType

    def delete(self, id: uuid.UUID) -> None:
        session: Session = self._dbcontext.createSession()
        record = session.query(TicketTypeModel).filter(TicketTypeModel.id == id).first()
        if not record:
            session.close()
            return None
        session.delete(record)
        session.commit()
        session.close()
        return None

    def getall(self) -> List[TicketType]:
        response: List[TicketType] = list()
        session: Session = self._dbcontext.createSession()
        query = select(TicketType)
        records = session.execute(query).fetchall()
        for record in records:
            entity: TicketType = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response

    def get_by_name(self, name: str) -> Optional[TicketType]:
        session: Session = self._dbcontext.createSession()
        record = session.query(TicketTypeModel).filter(TicketTypeModel.name == name).first()
        session.close()
        if not record:
            return None
        entity = self._to_entity(record)
        return entity

    def get_by_id(self, id: uuid.UUID) -> Optional[TicketType]:
        session: Session = self._dbcontext.createSession()
        record = session.query(TicketTypeModel).filter(TicketTypeModel.id == id).first()
        session.close()
        if not record:
            return None
        entity = self._to_entity(record)
        return entity

    # def search_by_name(self, term: str) -> List[TicketType]:
    #     return self._find(TicketTypeModel.name.icontains(term, autoescape=True))

    # def get_by_price_range(self, min_price: float, max_price: float) -> List[TicketType]:
    #     return self._find(TicketTypeModel.price.between(min_price, max_price))