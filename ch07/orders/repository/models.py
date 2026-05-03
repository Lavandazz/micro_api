"""
Модели для sqlalchemy.
Создание миграций: alembic revision --autogenerate -m "Initial migration"
Применение миграций: alembic upgrade head

Удаление миграций: rm -f migrations/versions/*.py    
Удалит все миграции. Важно учитывать в какой миграции на данный момент находится база и откатить до рабочей версии: 
alembic downgrade base - откат к пустой базе
alembic downgrade 123abc456 - откат до определенной миграции
alembic history - Просмотр истории миграций

"""

import uuid
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, Integer


class Base(DeclarativeBase):
    pass


def generate_uuid():
    return str(uuid.uuid4())


class OrderModel(Base):
    __tablename__ = "order"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    items: Mapped[list["OrderItemModel"]] = relationship("OrderItemModel", backref="order")
    status: Mapped[str] = mapped_column(String, nullable=False, default="created")
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    schedule_id: Mapped[str] = mapped_column(String)
    delivery_id: Mapped[str] = mapped_column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "items": [item.dict() for item in self.items],
            "status": self.status,
            "delivery_id": self.delivery_id
        }
    
class OrderItemModel(Base):
    __tablename__ = "order_item"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("order.id"))
    product: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product,
            "size": self.size,
            "quantity": self.quantity
        }

