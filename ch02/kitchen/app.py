"""
Реализация роутов для планирования заказов с помощью Flask, marshmallow.
В файле ch02/kitchen/oas.yaml описаны схемы для планирования заказа ScheduleOrderSchema, 
для предоставления сведений о запланированном заказе - GetScheduledOrderSchema,
и представление о товаре в заказе OrderItemSchema.

Запуск Flask осуществляется с помощью команды flask run или flask run --debug
В файле ch02/kitchen/api/schemas.py определяются схемы с помощью моделей marshmallow.
"""

from flask import Flask
from flask_smorest import Api

from ch02.kitchen.api.api import blueprint
from . config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)

kitchen_api = Api(app)
kitchen_api.register_blueprint(blueprint)
