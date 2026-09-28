import uuid
import os
from fastapi import APIRouter, HTTPException, status, Response
from api.infrastructure.postgres.dbcontext import DBContext
from api.models.order import Order
from api.models.order_repository import OrderRepository

router = APIRouter(tags=["orders"])

@router.post("/orders", status_code=status.HTTP_201_CREATED | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def create_order(res: Response, payload: Order) -> Order:
    dbcontext: DBContext = DBContext(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], username=os.environ['DB_UID'], password=os.environ['DB_PWD'])
    orderRepo: OrderRepository = OrderRepository(dbcontext=dbcontext)
    response = orderRepo.add(payload)
    res.status_code = status.HTTP_201_CREATED
    return response