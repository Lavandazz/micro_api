"""
Реализация патерная Единица работы для подключения к бд.
Пример работы%
with UnitOfWork as uow:
    repo = SqlAlchemyOrdersRepository(uow.session) - получаем экземпляр sqlalchemy для работы с заказами
    orders_service = OrderService(repo)
    ...
    Дальнейшая работа с заказами
    uow.commit() - сохранение заказа

Используется в DI (dependencies.py)
"""
from sqlalchemy.orm import sessionmaker


class UnitOfWork:
    def __init__(self, session_maker):
        """Инициация подключения к бд"""
        # self.session_maker = sessionmaker(bind=create_engine(f"sqlite:///{os.getenv("db")}.db"))
        self.session_maker: sessionmaker = session_maker # Передаем готовый sessionmaker

    def __enter__(self):
        """Открытие новой сесси в блоке with"""
        self.session = self.session_maker() # Открытие нового сеанса работы с бд
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None: # Проверка, есть ли исключения, если есть, то откатываем изменения и закрываем соединение.
            self.rollback()
            self.session.close()
        else:
            self.session.commit()
            
        self.session.close()
    

    def commit(self):
        self.session.commit()

    def rollback(self):
        """Откат транзакции"""
        self.session.rollback()

    def close(self):
        pass
