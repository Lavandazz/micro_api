from datetime import datetime
from http import HTTPStatus
from typing import List, Optional
from uuid import uuid4

from fastapi import HTTPException
from pydantic import UUID4
from starlette import status
from starlette.responses import Response

from ch07.orders.orders_service.order_service import OrderService
from ch07.orders.repository.orders_repository import SqlAlchemyOrdersRepository
from ch07.orders.repository.unit_of_work import UnitOfWork
from ch07.orders.web.api.schemas import CreateOrderSchema, GetOrderSchema, GetOrdersSchema, OrderItemSchema


from typing import Annotated
from fastapi import APIRouter, Depends

from ch07.orders.web.dependencies import get_alchemy_orders_repository, get_uow

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
    print("results", results)
    return {
        "orders": [result.dict() for result in results]
    }

@router.post("/orders", response_model=GetOrderSchema)
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

@router.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(
    repo: Annotated[SqlAlchemyOrdersRepository, Depends(get_alchemy_orders_repository)],
    order_id: UUID4,
    ):
    orders_service = OrderService(repo)
    order = orders_service.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    


@router.post("/orders", response_model=GetOrderSchema)
def create_order(
    repo: Annotated[SqlAlchemyOrdersRepository, Depends(get_alchemy_orders_repository)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],                     # ← добавили uow
    payload: CreateOrderSchema
):
    orders_service = OrderService(repo)
    order_model = orders_service.add_order(payload.order)   # order_model – это ORM-объект
    uow.commit()                                            # ← фиксируем изменения

    # Формируем ответ согласно GetOrderSchema
    # Поле order: список товаров из payload (они уже в нужном формате)

    
    return GetOrderSchema(
        id=order_model.id,
        created=order_model.created,
        status=order_model.status,
        order=[OrderItemSchema(**item.dict()) for item in payload.order]
    )


@router.put(
    "/orders/{order_id}",
    response_model=GetOrderSchema,
    status_code=status.HTTP_200_OK
)
def update_order(repo: Annotated[SqlAlchemyOrdersRepository, Depends(get_alchemy_orders_repository)],
                 order_id: UUID4, order_details: CreateOrderSchema):
    orders_service = OrderService(repo)
    order = orders_service.get_order(order_id)

    if order['id'] == order_id:
        order.update(order_details.dict())

        return order
    raise HTTPException(status_code=404, detail="Order not found")


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(repo: Annotated[SqlAlchemyOrdersRepository, Depends(get_alchemy_orders_repository)],
                 order_id:  UUID4):
    orders_service = OrderService(repo)
    order = orders_service.get_order(order_id)
    if order['id'] == order_id:
        # ORDERS.pop(index)
        # return Response(status_code=status.NO_CONTENT.value)
        print("Удалил")

    raise HTTPException(status_code=404, detail="Order not found")


@router.post("/orders/{order_id}/cancel")
def cancel_order(repo: Annotated[SqlAlchemyOrdersRepository, Depends(get_alchemy_orders_repository)],
order_id:  UUID4):
    orders_service = OrderService(repo)
    order = orders_service.get_order(order_id)
    if order['id'] == order_id:
        order['status'] = 'cancelled'
        return order
    raise HTTPException(status_code=404, detail="Order not found")


@router.post("/orders/{order_id}/pay")
def pay_order(repo: Annotated[SqlAlchemyOrdersRepository, Depends(get_alchemy_orders_repository)],
order_id: UUID4):
    orders_service = OrderService(repo)
    order = orders_service.get_order(order_id)
    if order['id'] == order_id:
        order['status'] = 'paid'
        return order
    
    raise HTTPException(status_code=404, detail="Order not found")
