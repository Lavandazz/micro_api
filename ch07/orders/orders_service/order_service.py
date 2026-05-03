"""
Реализация паттерна "Внедрение зависимостей" для работы с заказами
"""

class OrderService:
    def __init__(self, orders_repository):
        """Получаем экземпляр репозитория для работы с бд"""
        self.orders_repository = orders_repository

    def place_order(self, order):
        pass

    def get_order(self, order_id):
        pass

    def update_order(self, order_id, items):
        pass

    def list_orders(self, **filters):
        pass

    def pay_order(self, order_id):
        pass

    def cancel_order(self, order_id):
        pass
    