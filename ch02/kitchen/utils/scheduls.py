from datetime import datetime


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