import uuid
from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import * # type: ignore
from api.infrastructure.postgres.dbcontext import DBContext
from api.models.orderitem import OrderItem
from api.infrastructure.postgres.orderitem import OrderItem as OrderItemModel
from api.infrastructure.postgres.orders import Order as OrderModel


class OrderItemRepository():
    def __init__(self, dbcontext: DBContext) -> None:
        self._dbcontext: DBContext = dbcontext

    def _to_entity(self, model: OrderItemModel) -> OrderItem:
        item = OrderItem(
            id=model.id,
            order_id=model.order_id,
            ticket_type_id=model.ticket_type_id,
            quantity=model.quantity,
            price=float(model.price)
        )
        return item

    def _to_model(self, entity: OrderItem) -> OrderItemModel:
        return OrderItemModel(
            id=entity.id,
            order_id=entity.order_id,
            ticket_type_id=entity.ticket_type_id,
            quantity=entity.quantity,
            price=entity.price,
        )

    def add(self, orderItem: OrderItem, session: Optional[Session] = None) -> OrderItem:  # type: ignore[override]
        owns_session = session is None
        session = session or self._dbcontext.createSession()
        try:
            entity = self._to_model(orderItem)
            session.add(entity)
            if owns_session:
                session.commit()
        except Exception:
            if owns_session:
                session.rollback()
            raise
        finally:
            if owns_session:
                session.close()
        return orderItem

    def update(self, orderItem: OrderItem) -> Optional[OrderItem]:  # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        record = session.query(OrderItemModel).filter(OrderItemModel.id == orderItem.id).first()
        if not record:
            session.close()
            return None
        record.order_id = orderItem.order_id
        record.price = Decimal(orderItem.price)
        record.quantity = orderItem.quantity
        record.ticket_type_id = orderItem.ticket_type_id
        session.commit()
        session.close()
        return orderItem

    def delete(self, id: uuid.UUID) -> None:
        session: Session = self._dbcontext.createSession()
        record = session.query(OrderItemModel).filter(OrderItemModel.id == id).first()
        if not record:
            session.close()
            return None
        session.delete(record)
        session.commit()
        session.close()
        return None

    def getall(self) -> List[OrderItem]:
        response: List[OrderItem] = list()
        session: Session = self._dbcontext.createSession()
        query = select(OrderItemModel)
        records = session.execute(query).fetchall()
        for record in records:
            entity: OrderItem = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response
    
    def get_by_order_id(self, order_id: uuid.UUID) -> List[OrderItem]:
        response: List[OrderItem] = list()
        session: Session = self._dbcontext.createSession()
        query = select(OrderItemModel).filter(OrderItemModel.order_id == order_id)
        records = session.execute(query).fetchall()
        for record in records:
            entity: OrderItem = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response
