"""
Запуск сервера из папки ch07:
uvicorn orders.web.app:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(debug=True)

# Переопределение json файлов и openapi схем
# app = FastAPI(debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders")

# Чтение yaml файла
# oas_doc = yaml.safe_load(
#     API_YAML.read_text(encoding="utf-8") 
# )

# Переопределение свойств openapi
# app.openapi = lambda: oas_doc
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# from ch07.orders.api import api
