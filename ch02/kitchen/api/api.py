from datetime import datetime
import uuid

from flask import abort
from flask_smorest import Blueprint
from flask.views import MethodView

# from ch02.kitchen.utils.utils import get_schedule

from ..utils.utils import get_schedule
from ..utils.scheduls import shedules
from .schemas import GetKitchenScheduleParameters, GetSheduleOrderShema, GetSheduledOrdersSchema, SheduleOrderSchema, SheduleStatusSchema


blueprint = Blueprint(name="kitchen", import_name=__name__, description="Kitchen")


@blueprint.route("/kitchen/schedules")
class KitchenSHedules(MethodView):
    """
    Класс для отображения информации о заказах, а так же для создания конкретного заказа
    """
    @blueprint.arguments(schema=GetKitchenScheduleParameters, location="query") # добавляем параметры в URL запрос
    @blueprint.response(status_code=200, schema=GetSheduledOrdersSchema)
    def get(self, parameters):
        """Отображение всех заказов"""
        # for sh in shedules:
        #     validate_schedule(sh)

        if not parameters:
            return {
                "shedules": shedules
            }
        query_set = [shed for shed in shedules]

        cancelled = parameters.get("cancelled")
        if cancelled is not None:
            if cancelled:
                query_set = [
                    shed
                    for shed in shedules
                    if shed["status"] == "cancelled"
                ]
            else:
                query_set = [
                    shed
                    for shed in shedules
                    if shed["status"] != "cancelled"
                ]

        since = parameters.get("since")
        if since is not None:
            query_set = [
                shed for shed in shedules if shed["scheduled"] >= since
            ]

        limit = parameters.get("limit")
        if limit is not None and len(query_set) > limit:
            query_set = query_set[:limit]

        return {"shedules": query_set}

    
    @blueprint.arguments(schema=SheduleOrderSchema)
    @blueprint.response(status_code=201, schema=GetSheduleOrderShema)
    def post(self, payload):
        """Создание конкретного заказа"""
        payload["id"] = str(uuid.uuid4())
        payload["scheduled"] = datetime.now()
        payload["status"] = "pending"
        shedules.append(payload)
        return payload
    

@blueprint.route("/kitchen/schedules/<schedule_id>")
class KitchenSHedule(MethodView):
    """
    Класс для работы с конкретными заказами.
    Получение, изменение, удаление
    """
    @blueprint.response(status_code=200, schema=GetSheduleOrderShema)
    def get(self, schedule_id):
        """
        Отображение конкретного заказа.
        Если заказа не существует, фласк вернет 404 с  body {"code": 404, "status": "Not Found"}
        """
        result = get_schedule(schedule_id)
        print("result = ", result)
        if result:
            return result[0] # Возвращаем 0 элемент, тк result это список
        
        abort(404, description=f"Заказа № {schedule_id} не существует")
        
    @blueprint.arguments(schema=SheduleOrderSchema) # декоратор проверяет данные в соответствии со схемой
    @blueprint.response(status_code=200, schema=GetSheduleOrderShema) # декоратор отправляет данные и статус
    def put(self, order, schedule_id):
        """
        Изменение конкретного заказа
        order - словарь с конкретным товаром {'order': [{'product': 'coff', 'size': 'big', 'quantity': 1}]}
        """
        result = get_schedule(schedule_id)
        if result:
            result[0].update(order) # Обращаемся к 0 элементу списка, т.е к словарю
            return result[0]
        
        abort(404, description=f"Заказа № {schedule_id} не существует")
        
    
    @blueprint.response(status_code=200)
    def delete(self, schedule_id):
        """Удаление заказа"""
        index_for_delete = get_schedule(schedule_id, True) #  индекс для удаляения

        if index_for_delete:
            shedules.pop(index_for_delete[0])
            print(f'Удалено успешно {schedule_id}')
            return
            
        abort(404, description=f"Заказа № {schedule_id} не существует")


@blueprint.response(status_code=200, schema=GetSheduleOrderShema)
@blueprint.route("/kitchen/schedules/<schedule_id>/cancel", methods=["POST"])
def cancel_schedule(schedule_id):
    """Отмена заказа. """
    schedule = get_schedule(schedule_id)
    if schedule:
        schedule[0]["status"] = "cancelled"

        return shedules[0]
    
    abort(404, description=f"Заказа № {schedule_id} не существует")

@blueprint.response(status_code=200, schema=SheduleStatusSchema)
@blueprint.route("/kitchen/schedules/<schedule_id>/status", methods=["GET"])
def get_schedul_status(schedule_id):
    """Отображение статуса заказа"""
    schedule = get_schedule(schedule_id)
    if schedule:
        return {"status": schedule[0]["status"]}
