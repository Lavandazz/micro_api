from datetime import datetime
import uuid

from flask_smorest import Blueprint
from flask.views import MethodView


blueprint = Blueprint(name="kitchen", import_name=__name__, description="Kitchen")


shedules = [
    {  
    #   "id": str(uuid.uuid4()),
      "id": "846923e8-60c7-4b8f-844d-497555fbdf2a",
      "scheduled": datetime.now(),
      "status": "pending",
      "order":
        {
          "product": "capuccino",
          "quantity": 1,
          "size": "small"
        }
    },
    {  
    #   "id": str(uuid.uuid4()),
      "id": "3bab8700-1d32-4031-82a7-37afbdce6d5a",
      "scheduled": datetime.now(),
      "status": "pending",
      "order":
        {
          "product": "coffee",
          "quantity": 1,
          "size": "medium"
        }
    }
]


@blueprint.route("/kitchen/schedules")
class KitchenSHedules(MethodView):
    def get(self):
        print("апи работает")
        return {
            "shedules": shedules
        }, 200
    
    def post(self):
        return shedules, 201
    

@blueprint.route("/kitchen/schedules/<schedule_id>")
class KitchenSHedule(MethodView):
    def get(self, schedule_id):
        result = [sh_id for sh_id in shedules if sh_id.get("id") == schedule_id]
        if result:
            return result[0], 200
        else:
            return "Заказа не существует", 404
    
    def put(self, payload, schedule_id):
        # print("Оплата", schedule_id, payload)
        return shedules[0], 200
    
    def delete(self, schedule_id):
        return f'Удалено {schedule_id}', 204


@blueprint.route("/kitchen/schedules/<schedule_id>/cancel", methods=["POST"])
def cancael_schedule(schedule_id):
    return shedules[0], 200


@blueprint.route("/kitchen/schedules/<schedule_id>/status", methods=["GET"])
def get_schedul_status():
    return shedules[0], 200
