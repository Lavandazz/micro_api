from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, conint, conlist, field_validator

class Size(str, Enum):
    small = 'small'
    medium = 'medium'
    big = 'big'


class Status(str, Enum):
    created = 'created'
    processed = 'processed'
    cancelled = 'cancelled'
    dispatched = 'dispatched'
    delivered = 'delivered'


class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Optional[conint(ge=1, strict=True)] = 1  # Указывается минимальное значение и по умолчанию

    @field_validator('quantity')
    def validate_quantity(cls, value):
        assert value is not None, 'Количество не может быть None'
        return value

class CreateOrderSchema(BaseModel):
    order: conlist(OrderItemSchema, min_length=1)

class GetOrderSchema(BaseModel):
    orders: List[OrderItemSchema]