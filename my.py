# from marshmallow import EXCLUDE, Schema, fields, post_load
# from dataclasses import dataclass, field
# import datetime as dt


# @dataclass
# class User:
#     name: str
#     email: str
#     created_at: dt.datetime = field(default_factory=dt.datetime.now)

# class UserSchema(Schema):
#     name = fields.Str()
#     email = fields.Email()
#     created_at = fields.DateTime()

#     class Meta:
#         unknown = EXCLUDE

#     @post_load
#     def make_user(self, data, **kwargs):
#         return User(**data)


# user_data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
# schema = UserSchema()
# result = schema.load(user_data)
# print(result.name)

from datetime import datetime

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

    order = fields.Nested((OrderItemSchema), required=True)


shedules = [{  
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
    }]

order_schema = OrderItemSchema()
product = order_schema.load({"product": "capuccino", "quantity": 1,
          "size": "small"})

schema = SheduleOrderSchema()
# result = order_schema.load({"order": product})

print(product)
