from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, conint, conlist, field_validator


class Size(Enum):
    small = 'small'
    medium = 'medium'
    big = 'big'


class Status(Enum):
    created = 'created'
    processed = 'processed'
    cancelled = 'cancelled'
    dispatched = 'dispatched'
    delivered = 'delivered'


class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Optional[conint(ge=1, strict=True)] = 1  # Указывается минимальное значение и по умолчанию

    # Запрета свойств, которые не определены в схеме
    # forbid - полностью запрещает дополнительные данные
    # ignore - игнорирует дополнительные данные
    # allow - разрешает дополнительные данные
    model_config = ConfigDict(extra='forbid')

    @field_validator('quantity')
    def validate_quantity(cls, value):
        assert value is not None, 'Количество не может быть None'
        return value

class CreateOrderSchema(BaseModel):
    # Указываем, что в заказе минимальное количество товаров по умолчанию 1
    order: conlist(OrderItemSchema, min_length=1)

    model_config = ConfigDict(extra='forbid')


class GetOrderSchema(BaseModel):
    id: UUID
    created: datetime
    status: Status
    order: List[OrderItemSchema]  # возвращаем состав заказа


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]
