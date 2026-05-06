"""
Реализация паттерна Репозиторий
"""

from datetime import datetime
from uuid import uuid4

from ch07.orders.orders_service.orders import Order
from ch07.orders.repository.models import OrderModel, OrderItemModel

from abc import ABC, abstractmethod


class AbstractOrdersRepository(ABC):
    """
    Реализация абстрактного класса для патерна Репозиторий.
    Используется для работы с Tortoise ORM или для чистого подключения черех Postgresql.
    Описывает методы для работы с бд
    """
    @abstractmethod
    def add(self, items):
        pass

    @abstractmethod
    def get(self, id_):
        pass

    @abstractmethod
    def update(self, id_):
        pass

    @abstractmethod
    def delete(self, id_):
        pass


class SqlAlchemyOrdersRepository(AbstractOrdersRepository):
    """
    Тот же OrdersRepository
    session - зависимость от session sqlalchemy. Это объект sqlalchemy
    """
    def __init__(self, session) -> None:
        self.session = session

    def add(self, items):
        """
        Создание заказа в бд.
        items —  OrderItemSchema(product='coffee', size=<Size.big: 'big'>, quantity=1)
        order_model - объект модели бд OrderModel, который будет сохранен в бд. Он создается на основе данных из items, а также генерируется id и created.
        records - список объектов модели бд OrderItemModel, которые будут сохранены в бд
        """
        print("Получил items", items)

        order_model = OrderModel(
            id=str(uuid4()),
            status="created",
            created=datetime.now(),      # или datetime.utcnow()
            schedule_id=None,
            delivery_id=None,
        )

        records = [
            OrderItemModel(
                id=str(uuid4()),
                order_id=order_model.id,
                product=item.product,
                size=str(item.size.value),   # должно быть строкой,  i
                                            # item.size.value - это значение перечисления, например "big", 
                                            # а не объект перечисления Size.big
                quantity=item.quantity,
            )
            for item in items
        ]
      
        for record in records:
            self.session.add(record) # Добавляем запись в объекст session

        return order_model
    
    def _get(self, id_):
        return self.session.query(OrderModel).filter(OrderModel.id == str(id_)).first()
    
    def get(self, id_):
        """Получение всех заказов"""
        order = self._get(id_)
        print("SqlAlchemyOrdersRepository - order", order)
        if order is not None:
            return Order(**order.dict())

    def list_orders(self, limit=None, **filters):
        """
        Получение саиска заказов
        """
        query = self.session.query(OrderModel)
        if "cancelled" in filters:
            cancelled = filters.pop("cancelled")
            if cancelled:
                query = query.filter(OrderModel.status == "cancelled")
            else:
                query = query.filter(OrderModel.status != "cancelled")

        records = query.filter_by(**filters).limit(limit).all()
        return [Order(**record.dict()) for record in records]
    
    def update(self, id_, **payload):
        """
        Для изменения заказа, сначала удаляются необходимые элементы, затем вставляются новые значения
        """
        record = self._get(id_)
        if 'items' in payload:
            for item in record.items():
                self.session.delete(item)
            record.items = [
                OrderItemModel(**item) for item in payload.pop("item")
            ]
        for key, value in payload.items():
            setattr(record, key, value)
        
        return Order(**record.dict())
    
    def delete(self, id_):
        """Удаление заказа"""
        self.session.delete(id_)

