from fastapi import FastAPI

app = FastAPI(debug=True)

from ch02.orders.api import api