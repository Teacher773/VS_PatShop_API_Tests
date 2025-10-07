import allure
import jsonschema
import pytest
import requests
import json
from Tests.schemas.store_schema import STORE_SCHEMA
from Tests.schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_add_order(self):
        with allure.step("Подготовка данных для отправки"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
        with allure.step("Отправка запроса"):
            response = requests.post(
                url=f"{BASE_URL}/store/order",
                json=payload,
                headers={"Content-Type": "application/json"})

            response_json = response.json()

        with allure.step("Проверка ответа и валидация json - схемы"):
            assert response.status_code == 200
            jsonschema.validate(instance=response_json, schema=STORE_SCHEMA)

        with allure.step("Проверка размещения заказа в ответе"):
            assert response_json["id"] == payload["id"] == 1, "id не совпадает"
            assert response_json["petId"] == payload["petId"] == 1, "petId не совпадает"
            assert response_json["quantity"] == payload["quantity"] == 1, "кол-во не совпадает"
            assert response_json["status"] == payload["status"] == "placed", "статус не совпадает"
            assert response_json["complete"] == payload["complete"] == True, "Объем не совпадает"

    @allure.title("Получение информации о заказе по id")
    def test_get_order_by_id(self, create_order):
        with allure.step("Отправка запроса на получение данных о заказе по id "):
            response = requests.get(
                url=f"{BASE_URL}/store/order/{create_order["id"]}")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200
            assert create_order["id"] == 1, "id не совпадает"
            assert create_order["petId"] == 1, "petId не совпадает"
            assert create_order["quantity"] == 1, "кол-во не совпадает"
            assert create_order["status"] == "placed", "статус не совпадает"
            assert create_order["complete"] == True, "Объем не совпадает"

    @allure.title("Удаление заказа по id")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Отправка запроса на удаление заказа"):
            response = requests.delete(
                url=(
                    f"{BASE_URL}/store/order/{create_order['id']}")
            )

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Статус код не совпадает с ожидаемым"

        with allure.step("Проверка статуса кода на получение удаленного заказа"):
            response = requests.get(
                f"{BASE_URL}/store/order/{create_order["id"]}")
            assert response.status_code == 404, "Статус код не совпадает с ожидаемым"

    @allure.title("Получение несуществующего заказа")
    def test_get_nonexistent_order(self):
        with allure.step("Проверка статуса кода на получение удаленного заказа"):
            response = requests.get(
                f"{BASE_URL}/store/order/9999")
            assert response.status_code == 404, "Статус код не совпадает с ожидаемым"
            assert response.text == "Order not found"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря"):
            response = requests.get(
                f"{BASE_URL}/store/inventory")

            response_json = response.json()

        with allure.step("Проверка статуса кода и валидации формата ответа"):
            assert response.status_code == 200, "Статус код не совпадает с ожидаемым"
            jsonschema.validate(instance=response_json, schema=INVENTORY_SCHEMA)




