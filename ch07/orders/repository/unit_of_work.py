"""
Реализация патерная Единица работы для подключения к бд.
Пример работы%
with UnitOfWork as uow:
    repo = SqlAlchemyOrdersRepository(uow.session) - получаем экземпляр sqlalchemy для работы с заказами
    orders_service = OrderService(repo)
    ...
    Дальнейшая работа с заказами
    uow.commit() - сохранение заказа
"""
import os
from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path_env = Path.cwd() / ".env"
load_dotenv(path_env)


class UnitOfWork:
    def __init__(self):
        """Инициация подключения к бд"""
        self.session_maker = sessionmaker(bind=create_engine(f"sqlite:///{os.getenv("db")}.db"))

    def __enter__(self):
        self.session = self.session_maker() # Открытие нового сеанса работы с бд
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None: # Проверка, есть ли исключения, если есть, то откатываем изменения и закрываем соединение.
            self.rollback()
            self.session.close()
        self.session.close()
    

    def commit(self):
        self.session.commit()

    def rollback(self):
        """Откат транзакции"""
        self.session.rollback()

        