import uuid
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from ch02.orders.app import app
from ch02.orders.api.schemas import CreateOrderSchema, GetOrdersSchema, GetOrderSchema

ORDERS = []
order = {
    'id': 'ff0f1355-e821-4178-9567-550dec27a373',
    'status': 'delivered',
    'created': datetime.now(),
    'order': {
        'product': 'capuccino',
        'size': 'medium',
        'quantity': 1,
    }
}

@app.get("/orders", response_model=GetOrdersSchema)
def get_orders():

    if ORDERS:
        print('Заказы', ORDERS)
        return {'orders': ORDERS}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Список заказов пуст')


@app.post(
    "/orders", response_model=GetOrderSchema,
    status_code=status.HTTP_201_CREATED
)
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    order['id'] = uuid.uuid4()
    order['created'] = datetime.now()
    order['status'] = 'created'
    ORDERS.append(order)
    return order


@app.get(
    "/orders/{order_id}", response_model=GetOrderSchema,
    status_code=status.HTTP_200_OK
)
def get_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")


@app.put(
    "/orders/{order_id}",
    response_model=GetOrderSchema,
    status_code=status.HTTP_200_OK
)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in ORDERS:
        if order['id'] == order_id:
            order.update(order_details.dict())

            return order
    raise HTTPException(status_code=404, detail="Order not found")


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    for index, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(index)
            return Response(status_code=status.NO_CONTENT.value)
    raise HTTPException(status_code=404, detail="Order not found")


@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'cancelled'
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.post("/orders/{order_id}/pay")
def pay_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'paid'
            return order
    raise HTTPException(status_code=404, detail="Order not found")
