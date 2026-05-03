

from ch07.orders.repository.models import OrderModel


class Order:
    """
    Класс, представляющий элемент заказа.
    schedule_id, delivery_id, _status - считаются None, 
    тк класс используется до и после сохранения заказа. Данные свойства становятся известны
    только после создания заказа.
    order_ - экземпляр модели бд OrderModel
    """
    def __init__(self, id, created, items, status, schedule_id=None,
                 delivery_id=None, order_=None) -> None:
        self._order: OrderModel = order_
        self._id = id
        self._created = created
        self.items = [OrderItem(**item) for item in items] # создаем объект для каждого элемента заказа
        self._status = status
        self.schedule_id = schedule_id
        self.delivery_id = delivery_id
 
    @property
    def id(self):
        return self._id or self._order.id 
    
    @property
    def created(self):
        return self._created or self._order.created
    
    @property
    def status(self):
        return self._status or self._order.status

    

class OrderItem:
    """
    Класс, представляющий элемент продукта.
    """
    def __init__(self, id, product, size, quantity):
        self.id = id
        self.product = product
        self.size = size
        self.quantity = quantity
