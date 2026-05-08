"""
Реализация паттерна "Внедрение зависимостей" для работы с заказами
"""

from ch07.orders.orders_service.exceptions import OrderNotFoundError


class OrderService:
    def __init__(self, orders_repository):
        """Получаем экземпляр репозитория для работы с бд"""
        self.orders_repository = orders_repository # Передается экземпляр ORM (SqlAlchemyOrdersRepository)

    def add_order(self, order):
        """Создание заказа в бд"""
        return self.orders_repository.add(order)

    def get_order(self, order_id):
        """Получение заказа"""
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError("Заказа № %s не существует" % order_id)
        return order

    def update_order(self, order_id, items):
        """Обновление заказа"""
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError("Заказа № %s не существует" % order_id)
        return self.orders_repository.update(order, {"items": items})
        
    def list_orders(self, **filters):
        """Запись фильтров"""
        limit = filters.pop("limit", None)
        return self.orders_repository.get_orders(limit, **filters)

    def pay_order(self, order_id):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError("Заказа № %s не существует" % order_id)
        order.pay()
        schedule_id = order.schedule()
        return self.orders_repository.update(
            order_id, {"status":"scheduled", "schedule_id": schedule_id}
        )

    def cancel_order(self, order_id):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError("Заказа № %s не существует" % order_id)
        
        order.cancel()
        return self.orders_repository.update(order_id, status="cancelled")
    