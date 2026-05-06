from datetime import datetime
from http import HTTPStatus
from typing import List, Optional
from uuid import uuid4

from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from ch07.orders.orders_service.order_service import OrderService
from ch07.orders.repository.orders_repository import SqlAlchemyOrdersRepository
from ch07.orders.web.api.schemas import CreateOrderSchema, GetOrdersSchema


from typing import Annotated
from fastapi import APIRouter, Depends

from ch07.orders.web.dependencies import get_alchemy_orders_repository

router = APIRouter()

mock_orders = [
    {  
    #   "id": str(uuid.uuid4()),
      "id": "846923e8-60c7-4b8f-844d-497555fbdf2a",
      "created": datetime.now(),
      "status": "pending",
      "order":
        [{
          "product": "capuccino",
          "size": "small",
          "quantity": 1,
        },
        {
            "product": "croissant",
            "size": "medium",
            "quantity": 2
        }]
    },
    {  
    #   "id": str(uuid.uuid4()),
      "id": "3bab8700-1d32-4031-82a7-37afbdce6d5a",
      "created": datetime.now(),
      "status": "pending",
      "order":[
        {
          "product": "coffee",
          "quantity": 1,
          "size": "medium"
        }]
    }
]

@router.get("/orders", response_model=GetOrdersSchema)
def get_orders(
    repo: Annotated[SqlAlchemyOrdersRepository, Depends(get_alchemy_orders_repository)],
    cancelled: Optional[bool]=None,
    limit: Optional[int]=None
    ):

    orders_service = OrderService(repo)
    results = orders_service.list_orders(
        cancelled=cancelled, limit=limit
    )
    
    # if not results:
    #     results = mock_orders
    #     return results

    print("results", results)
    return {
        "orders": [result.dict() for result in results]
    }

@router.post("/orders") # response_model=GetOrdersSchema
def create_order(
    repo: Annotated[SqlAlchemyOrdersRepository, Depends(get_alchemy_orders_repository)],
    payload: CreateOrderSchema
    ):
    orders_service = OrderService(repo)
    print("PAYLOAD, ", payload)

    # payload.order имеет вид [OrderItemSchema(product='coffee', size=<Size.big: 'big'>, quantity=1)]
    # Преобразуем и сохраняем заказ в бд, а также получаем объект OrderModel с данными из бд, 
    # включая id и created, которые генерируются при сохранении заказа
    order = orders_service.add_order(payload.order) 
    
    return order


