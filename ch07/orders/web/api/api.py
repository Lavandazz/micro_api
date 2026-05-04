from http import HTTPStatus
from typing import List, Optional
from uuid import uuid4

from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from ch07.orders.orders_service.order_service import OrderService
from ch07.orders.repository.orders_repository import SqlAlchemyOrdersRepository
from ch07.orders.repository.unit_of_work import UnitOfWork
from ch07.orders.web.api.schemas import GetOrdersSchema



from fastapi import APIRouter

router = APIRouter()

@router.get("/orders", response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool]=None,
               limit: Optional[int]=None,):
    with UnitOfWork() as uow: # Открытие сессии бд
        print("Внимание, получаю заказы")
        repo = SqlAlchemyOrdersRepository(uow.session) # получаем экземпляр sqlalchemy для работы с заказами в бд
        orders_service = OrderService(repo)
        results = orders_service.list_orders(
            cancelled=cancelled, limit=limit
        )
    return {
        "orders": [result.dict() for result in results]
    }

