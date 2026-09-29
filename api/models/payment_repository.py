import uuid
import datetime
from decimal import Decimal
from typing import Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import * # type: ignore
from api.infrastructure.postgres.dbcontext import DBContext
from api.models.payment import Payment
from api.infrastructure.postgres.payments import Payment as PaymentModel

UNKNOWN_PAYMENT_METHOD = "unknown"

class PaymentRepository():
    def __init__(self, dbcontext: DBContext) -> None:
        self._dbcontext: DBContext = dbcontext
    
    model_class = PaymentModel

    def _to_entity(self, model: PaymentModel) -> Payment:
        payment = Payment(
            id=model.id,
            user_id=model.user_id,
            order_id=model.order_id,
            amount=float(model.amount),
            status=model.status
        )
        return payment

    def _to_model(self, entity: Payment) -> PaymentModel:
        return PaymentModel(
            id=entity.id,
            user_id=entity.user_id,
            order_id=entity.order_id,
            amount=entity.amount,
            status=entity.status,
        )

    def add(self, payment: Payment) -> Payment: # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        entity = self._to_model(payment)
        session.add(entity)
        session.commit()
        session.close()
        return payment

    def update(self, payment: Payment) -> Optional[Payment]: # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        record = session.query(PaymentModel).filter(PaymentModel.id == payment.id).first()
        if not record:
            session.close()
            return None       
        record.status = payment.status
        record.order_id = payment.order_id
        record.user_id = payment.user_id
        record.amount = Decimal(payment.amount)
        session.commit()
        session.close()
        return payment

    def delete(self, id: uuid.UUID) -> None:
        session: Session = self._dbcontext.createSession()
        record = session.query(PaymentModel).filter(PaymentModel.id == id).first()
        if not record:
            session.close()
            return None
        session.delete(record)
        session.commit()
        session.close()
        return None   

    def getall(self) -> List[Payment]:
        response: List[Payment] = list()
        session: Session = self._dbcontext.createSession()
        query = select(PaymentModel)
        records = session.execute(query).fetchall()
        for record in records:
            entity: Payment = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response     

    def get_by_order_id(self, order_id: uuid.UUID) -> List[Payment]:
        response: List[Payment] = list()
        session: Session = self._dbcontext.createSession()
        query = select(PaymentModel).filter(PaymentModel.order_id == order_id)
        records = session.execute(query).fetchall()
        for record in records:
            entity: Payment = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response

    def get_by_user_id(self, user_id: uuid.UUID) -> List[Payment]:
        response: List[Payment] = list()
        session: Session = self._dbcontext.createSession()
        query = select(PaymentModel).filter(PaymentModel.user_id == user_id)
        records = session.execute(query).fetchall()
        for record in records:
            entity: Payment = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response

    def get_by_status(self, status: str) -> List[Payment]:
        response: List[Payment] = list()
        session: Session = self._dbcontext.createSession()
        query = select(PaymentModel).filter(PaymentModel.status == status)
        records = session.execute(query).fetchall()
        for record in records:
            entity: Payment = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response
