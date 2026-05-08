import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime

from ch02.orders.api.api import router  # или импортируйте ваше приложение FastAPI
from fastapi import FastAPI

# Собираем приложение для тестов (обычно это делается в conftest.py)
app = FastAPI()
app.include_router(router)
client = TestClient(app)

# Фикстура, которая перед каждым тестом создает чистый список заказов
@pytest.fixture(autouse=True)
def clean_orders():
    # Сохраняем оригинальный список
    from ch02.orders.api.api import ORDERS
    original = ORDERS.copy()
    # Для каждого теста используем заранее известные данные
    ORDERS.clear()
    ORDERS.extend([
        {
            "id": "9bf7e21e-7f59-4cc9-8146-659a6c474769",
            "created": "2026-05-06T15:00:17.855750",
            "status": "created",
            "order": [{"product": "coffee", "size": "small", "quantity": 1}]
        },
        {
            "id": "ff0f1355-e821-4178-9567-550dec27a373",
            "status": "delivered",
            "created": "2026-04-06T15:00:13.855750",
            "order": [{"product": "capuccino", "size": "medium", "quantity": 1}]
        }
    ])
    yield
    # После теста восстанавливаем (необязательно, если тесты не мешают друг другу)
    ORDERS.clear()
    ORDERS.extend(original)


# -------- Тесты для GET /orders --------
def test_get_orders_returns_all():
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert "orders" in data
    assert len(data["orders"]) == 2
    # Проверим, что поля соответствуют схеме GetOrderSchema
    assert data["orders"][0]["id"] == "9bf7e21e-7f59-4cc9-8146-659a6c474769"

def test_get_orders_filter_cancelled_true():
    # Сначала отменим один заказ
    client.post("/orders/9bf7e21e-7f59-4cc9-8146-659a6c474769/cancel")
    response = client.get("/orders?cancelled=true")
    assert response.status_code == 200
    orders = response.json()["orders"]
    assert len(orders) == 1
    assert orders[0]["status"] == "cancelled"

def test_get_orders_filter_cancelled_false():
    # cancelled=false - все, кроме отмененных
    client.post("/orders/9bf7e21e-7f59-4cc9-8146-659a6c474769/cancel")
    response = client.get("/orders?cancelled=false")
    assert response.status_code == 200
    orders = response.json()["orders"]
    assert len(orders) == 1
    assert orders[0]["status"] != "cancelled"

def test_get_orders_limit():
    response = client.get("/orders?limit=1")
    assert response.status_code == 200
    orders = response.json()["orders"]
    assert len(orders) == 1

def test_get_orders_empty_list():
    # Очищаем список (фикстура пересоздает, поэтому временно удалим)
    from ch02.orders.api.api import ORDERS
    ORDERS.clear()
    response = client.get("/orders")
    assert response.status_code == 404
    assert response.json()["detail"] == "Список заказов пуст"


# -------- Тесты для POST /orders --------
def test_create_order_success():
    new_order = {
        "order": [
            {"product": "tea", "size": "big", "quantity": 2}
        ]
    }
    response = client.post("/orders", json=new_order)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["status"] == "created"
    assert "created" in data
    assert data["order"] == new_order["order"]
    # Проверим, что заказ действительно добавился в список
    get_response = client.get("/orders")
    assert len(get_response.json()["orders"]) == 3

def test_create_order_invalid_quantity():
    new_order = {
        "order": [
            {"product": "tea", "size": "big", "quantity": 0}  # quantity < 1
        ]
    }
    response = client.post("/orders", json=new_order)
    assert response.status_code == 422  # Validation error


# -------- Тесты для GET /orders/{id} --------
def test_get_order_by_id_exists():
    order_id = "9bf7e21e-7f59-4cc9-8146-659a6c474769"
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id

def test_get_order_by_id_not_found():
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/orders/{fake_id}")
    assert response.status_code == 404


# -------- Тесты для PUT /orders/{id} --------
def test_update_order_success():
    order_id = "9bf7e21e-7f59-4cc9-8146-659a6c474769"
    update_data = {
        "order": [{"product": "latte", "size": "medium", "quantity": 3}]
    }
    response = client.put(f"/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["order"] == update_data["order"]

def test_update_order_not_found():
    fake_id = "00000000-0000-0000-0000-000000000000"
    update_data = {"order": [{"product": "latte", "size": "medium", "quantity": 1}]}
    response = client.put(f"/orders/{fake_id}", json=update_data)
    assert response.status_code == 404


# -------- Тесты для DELETE /orders/{id} --------
def test_delete_order_success():
    order_id = "9bf7e21e-7f59-4cc9-8146-659a6c474769"
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 204
    assert response.text == ""  # Нет содержимого
    # Проверяем, что заказа больше нет
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404

def test_delete_order_not_found():
    response = client.delete("/orders/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


# -------- Тесты для POST /cancel --------
def test_cancel_order():
    order_id = "9bf7e21e-7f59-4cc9-8146-659a6c474769"
    response = client.post(f"/orders/{order_id}/cancel")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"
    # Убедимся, что статус изменился в основном списке
    get_resp = client.get(f"/orders/{order_id}")
    assert get_resp.json()["status"] == "cancelled"


# -------- Тесты для POST /pay --------
def test_pay_order():
    order_id = "9bf7e21e-7f59-4cc9-8146-659a6c474769"
    response = client.post(f"/orders/{order_id}/pay")
    assert response.status_code == 200
    assert response.json()["status"] == "paid"