from marshmallow import ValidationError
from copy import deepcopy

from ch02.kitchen.api.schemas import GetSheduleOrderShema
from .scheduls import shedules

# Данную фунцию считаю лишней, 
# тк @blueprint.response(schema=GetSheduledOrdersSchema) сам проверит и преобразует данные
def validate_schedule(data):
    """
    Функция для валидации даты data["scheduled"] в строку формата ISO
    (из формата datetime.datetime(2026, 4, 28, 11, 8, 8, 328053) в 2026-04-28T11:08:08.328053)
    """
    print("Получил дату: ", data["scheduled"])
    data = deepcopy(data)
    data["scheduled"] = data["scheduled"].isoformat()
    print('schedule["scheduled"]= ', data["scheduled"], type(data["scheduled"]))
    errors = GetSheduleOrderShema().validate(data)

    if errors:
        raise ValidationError(errors)
    

def get_schedule(schedule_id, for_delete=False):
    """
    Функция возвращает заказ по айди.
    Для удаления заказа необходимо передать флаг for_delete=True
    """
    if not for_delete:
        result = [sh_id for sh_id in shedules if sh_id.get("id") == schedule_id]
        return result
    else:
        result = [index for index, sh_id in enumerate(shedules) if sh_id.get("id") == schedule_id]
        return result