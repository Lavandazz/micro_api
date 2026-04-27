from datetime import datetime
import uuid

from flask_smorest import Blueprint
from flask.views import MethodView

from .schemas import GetKitchenScheduleParameters, GetSheduleOrderShema, GetSheduledOrdersSchema, SheduleOrderSchema, SheduleStatusSchema


blueprint = Blueprint(name="kitchen", import_name=__name__, description="Kitchen")


shedules = [
    {  
    #   "id": str(uuid.uuid4()),
      "id": "846923e8-60c7-4b8f-844d-497555fbdf2a",
      "scheduled": datetime.now(),
      "status": "pending",
      "order":
        [{
          "product": "capuccino",
          "quantity": 1,
          "size": "small"
        },
        {
            "product": "croissant",
            "size": "medium",
            "quantity": 2
        }]
    },
    {  
    #   "id": str(uuid.uuid4()),
      "id": "3bab8700-1d32-4031-82a7-37afbdce6d5a",
      "scheduled": datetime.now(),
      "status": "pending",
      "order":[
        {
          "product": "coffee",
          "quantity": 1,
          "size": "medium"
        }]
    }
]


@blueprint.route("/kitchen/schedules")
class KitchenSHedules(MethodView):

    @blueprint.arguments(schema=GetKitchenScheduleParameters, location="query") # добавляем параметры в URL запрос
    @blueprint.response(status_code=200, schema=GetSheduledOrdersSchema)
    def get(self, parameters):
        """Отображение всех заказов"""
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
    def post(self):
        """Создание конкретного заказа"""
        return shedules
    

@blueprint.route("/kitchen/schedules/<schedule_id>")
class KitchenSHedule(MethodView):

    @blueprint.response(status_code=200, schema=GetSheduleOrderShema)
    def get(self, schedule_id):
        """Отображение конкретного заказа"""
        # result = [sh_id for sh_id in shedules if sh_id.get("id") == schedule_id]
        # if result:
        #     return result[0], 200
        # else:
        #     return "Заказа не существует", 404
        return shedules[0]
        
    @blueprint.arguments(schema=SheduleOrderSchema) # декоратор проверяет данные в соответствии со схемой
    @blueprint.response(status_code=200, schema=GetSheduleOrderShema) # декоратор отправляет данные и статус
    def put(self, payload, schedule_id):
        """Изенение конкретного заказа"""
        # print("Оплата", schedule_id, payload)
        return shedules[0]
    
    @blueprint.response(status_code=200)
    def delete(self, schedule_id):
        """Удаление заказа"""
        return f'Удалено успешно{schedule_id}'


@blueprint.response(status_code=200, schema=GetSheduleOrderShema)
@blueprint.route("/kitchen/schedules/<schedule_id>/cancel", methods=["POST"])
def cancel_schedule(schedule_id):
    """Отмена заказа"""
    return shedules[0]


@blueprint.response(status_code=200, schema=SheduleStatusSchema)
@blueprint.route("/kitchen/schedules/<schedule_id>/status", methods=["GET"])
def get_schedul_status():
    """Изменение статуса"""
    return shedules[0]
