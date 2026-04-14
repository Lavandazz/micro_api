from datetime import datetime
from uuid import UUID
from starlette.responses import Response
from starlette import status

from ch02.orders.app import app
from ch02.orders.api.schemas import CreateOrderSchema


orders = []
order = {
    'id': 'ff0f1355-e821-4178-9567-550dec27a373',
    'status': 'delivered',
    'created_at': datetime.now(),
    'order': {
        'product': 'capuccino',
        'size': 'medium',
        'quantity': 1,
    }
}

@app.get("/orders")
def get_orders():
    return {'orders': [orders]}


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order_details: CreateOrderSchema):
    return order


@app.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
def get_order(order_id: UUID):
    return order


@app.put("/orders/{order_id}", status_code=status.HTTP_200_OK)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    return order

@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    return Response(status_code=status.NO_CONTENT.value)


@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: UUID):
    return order

@app.post("/orders/{order_id}/pay")
def pay_order(order_id: UUID):
    return order