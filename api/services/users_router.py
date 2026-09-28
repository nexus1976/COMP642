import uuid
import os
from typing import List
from fastapi import APIRouter, HTTPException, status, Response
from api.infrastructure.postgres.dbcontext import DBContext
from api.models.user import User
from api.models.order import Order
from api.models.user_repository import UserRepository
from api.models.order_repository import OrderRepository

router = APIRouter(tags=["users"])

@router.get("/users", status_code=status.HTTP_200_OK | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def getall_users(res: Response) -> List[User]:
    dbcontext: DBContext = DBContext(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], username=os.environ['DB_UID'], password=os.environ['DB_PWD'])
    userRepo: UserRepository = UserRepository(dbcontext=dbcontext)
    response = userRepo.getall()
    res.status_code = status.HTTP_200_OK
    return response


@router.post("/users", status_code=status.HTTP_201_CREATED | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def create_user(res: Response, payload: User) -> User:
    dbcontext: DBContext = DBContext(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], username=os.environ['DB_UID'], password=os.environ['DB_PWD'])
    userRepo: UserRepository = UserRepository(dbcontext=dbcontext)
    response = userRepo.add(payload)
    res.status_code = status.HTTP_201_CREATED
    return response

@router.get("/users/{id}/orders", status_code=status.HTTP_200_OK | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def get_user_orders(res: Response, id: uuid.UUID) -> List[Order]:
    dbcontext: DBContext = DBContext(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], username=os.environ['DB_UID'], password=os.environ['DB_PWD'])
    orderRepo: OrderRepository = OrderRepository(dbcontext=dbcontext)
    response = orderRepo.get_by_user_id(id)
    res.status_code = status.HTTP_200_OK
    return response