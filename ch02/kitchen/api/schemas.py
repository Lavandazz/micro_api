from marshmallow import Schema, fields, validate, EXCLUDE


class OrderItemSchema(Schema):
    # Meta для запретанеизвестных свойств
    class Meta:
        unknown = EXCLUDE
    
    # required=True - говорит что поле является обязательным
    product = fields.String(required=True)
    size = fields.String(
        required=True, 
        validate=validate.OneOf(
            ["small", "medium", "big"]
            ))
    quantity = fields.Integer(
        validate=validate.Range(1, min_inclusive=True), required=True
    )

class SheduleOrderSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    # Отображение списка товаров, тк в заказе может быть несколько позиций (кофе, круассан)
    order = fields.List(fields.Nested(OrderItemSchema, required=True))

class GetSheduleOrderShema(SheduleOrderSchema):
    id = fields.UUID(required=True)
    scheduled = fields.DateTime(required=True)
    status = fields.String(
        required=True,
        validate=validate.OneOf(
            ["pending", "progress", "cancelled", "finished"]
            ))
    
class GetSheduledOrdersSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        
    shedules = fields.List(
        fields.Nested(GetSheduleOrderShema), required=True
    )

class SheduleStatusSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    status = fields.String(
        required=True,
        validate=validate.OneOf(
            ["pending", "progress", "cancelled", "finished"]
        )
    )

class GetKitchenScheduleParameters(Schema):
    """Добавление параметров запроса"""
    class Meta:
        unknown = EXCLUDE

    progress = fields.Boolean()
    limit = fields.Integer()
    since = fields.DateTime()
    