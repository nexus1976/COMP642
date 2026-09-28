import uuid
from decimal import Decimal
from typing import Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import * # type: ignore
from api.infrastructure.postgres.dbcontext import DBContext
from models.order import Order
from api.infrastructure.postgres.orders import Order as OrderModel

class OrderRepository():
    def __init__(self, dbcontext: DBContext) -> None:
        self._dbcontext: DBContext = dbcontext

    def _to_entity(self, model: OrderModel) -> Order:
        order = Order(
            id=model.id,
            user_id=model.user_id,
            event_id=model.event_id,
            total_amount=float(model.amount),
            status=model.status,
        )
        return order

    def _to_model(self, entity: Order) -> OrderModel:
        amount = Decimal(str(entity.total_amount))
        return OrderModel(
            id=entity.id,
            user_id=entity.user_id,
            event_id=entity.event_id,
            amount=amount,
            status=entity.status,
        )

    def add(self, order: Order) -> Order:  # type: ignore[override]
         session: Session = self._dbcontext.createSession()
         entity = self._to_model(order)
         session.add(entity)
         session.commit()
         session.close()
         return order

    def update(self, order: Order) -> Optional[Order]:  # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        record = session.query(OrderModel).filter(OrderModel.id == order.id).first()
        if not record:
            session.close()
            return None
        record.event_id = order.event_id
        record.user_id = order.user_id
        record.amount = Decimal(str(order.total_amount))
        record.status = order.status
        session.commit()
        session.close()
        return order

    def delete(self, id: uuid.UUID) -> None:
        session: Session = self._dbcontext.createSession()
        record = session.query(OrderModel).filter(OrderModel.id == id).first()
        if not record:
            session.close()
            return None
        session.delete(record)
        session.commit()
        session.close()
        return None    

    def get_by_user_id(self, user_id: uuid.UUID) -> List[Order]:
        response: List[Order] = list()
        session: Session = self._dbcontext.createSession()
        query = select(OrderModel).filter(OrderModel.user_id == user_id)
        records = session.execute(query).fetchall()
        for record in records:
            entity: Order = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response

    def get_by_id(self, id: uuid.UUID) -> Optional[Order]:
        session: Session = self._dbcontext.createSession()
        record = session.query(OrderModel).filter(OrderModel.id == id).first()
        session.close()       
        if not record:
            return None
        entity = self._to_entity(record)
        return entity