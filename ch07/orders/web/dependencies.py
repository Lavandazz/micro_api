import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Annotated

from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ch07.orders.repository.orders_repository import SqlAlchemyOrdersRepository
from ch07.orders.repository.unit_of_work import UnitOfWork


path_env = Path.cwd() / ".env" # Получаем env из папки ch07
load_dotenv(path_env)


engine = create_engine(f"sqlite:///{os.getenv("db")}.db")
session_maker = sessionmaker(bind=engine)


def get_uow():
    """ 
    Функция для подключения к бд
    """
    uow = UnitOfWork(session_maker)
    try:
        with uow: # вход в  __enter__ создаётся session
            yield uow # возврат открытой session
        # при выходе из with __exit__ сделает commit/rollback и закроет сессию
    finally:
        uow.close()


def get_alchemy_orders_repository(
        uow: Annotated[UnitOfWork, Depends(get_uow)]
        ):
    """ 
    Получение репозиторий алхимии для использования в DI
    """
    # Возвращаем сессию, тк SqlAlchemyOrdersRepository ожидает не объект UnitOfWork,
    # а именно session, которая создается внутри __enter__
    return SqlAlchemyOrdersRepository(uow.session)




