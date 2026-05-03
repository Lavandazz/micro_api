"""
Реализация паттерна Репозиторий
"""

from orders.orders_service.orders import Order
from orders.repository.models import OrderModel, OrderItemModel

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
        items — список словарей с товарами (product, size, quantity)
        """
        records = [OrderItemModel(**item) for item in items] # создаем запись для каждого элемента заказа

        for r in records: 
            self.session.add(r)
        # self.session.add(record) # Добавляем запись в объекст session

        return Order(**records.dict(), order=records) # Возвращаем экземпляр класса Order
    
    def _get(self, id_):
        return self.session.query(OrderModel).filter(OrderModel.id == str(id_)).first()
    
    def get(self, id_):
        order = self._get(id_)
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

