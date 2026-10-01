import uuid
import os
from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, status, Response
from api.infrastructure.postgres.dbcontext import DBContext
from api.models.order import Order
from api.models.orderitem import OrderItem
from api.models.order_item_repository import OrderItemRepository
from api.models.order_repository import OrderRepository

router = APIRouter(tags=["orders"])
EMPTY_UUID = uuid.UUID("00000000-0000-0000-0000-000000000000")

# THIS ENDPOINT DEMONSTRATES THE TRANSACTION REQUIRMENT IN PART A
@router.post("/orders", status_code=status.HTTP_201_CREATED | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def create_order(res: Response, payload: Order) -> Order:
    dbcontext: DBContext = DBContext(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], username=os.environ['DB_UID'], password=os.environ['DB_PWD'])
    orderRepo: OrderRepository = OrderRepository(dbcontext=dbcontext)
    orderItemRepo: OrderItemRepository = OrderItemRepository(dbcontext=dbcontext)
    session = dbcontext.createSession()
    try:
        if payload.id == EMPTY_UUID:
            payload.id = uuid.uuid4()
        orderRepo.add(payload, session=session)

        for order_item in payload.order_items:
            order_item.order_id = payload.id
            if order_item.id == EMPTY_UUID:
                order_item.id = uuid.uuid4()
            orderItemRepo.add(order_item, session=session)

        session.commit()
    except Exception as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create order and order items.",
        ) from exc
    finally:
        session.close()

    response = payload
    res.status_code = status.HTTP_201_CREATED
    return response

@router.get("/orders/{id}", status_code=status.HTTP_404_NOT_FOUND | status.HTTP_500_INTERNAL_SERVER_ERROR | status.HTTP_200_OK)
async def get_order(res: Response, id: uuid.UUID) -> Order | None:
    dbcontext: DBContext = DBContext(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], username=os.environ['DB_UID'], password=os.environ['DB_PWD'])
    orderRepo: OrderRepository = OrderRepository(dbcontext=dbcontext)
    order: Order | None = orderRepo.get_by_id(id)
    if not order:
        res.status_code = status.HTTP_404_NOT_FOUND
        return None

    orderItemRepo: OrderItemRepository = OrderItemRepository(dbcontext=dbcontext)
    items: List[OrderItem] = orderItemRepo.get_by_order_id(id)
    order.order_items = items
    res.status_code = status.HTTP_200_OK
    return order

    