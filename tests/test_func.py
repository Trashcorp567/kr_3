import json
from src.func import load_transactions_json
from src.func import sorted_operations_list
from src.func import date_convert
from src.func import card_number_send_from_hide
from src.func import card_number_send_to_hide
from src.func import operations_execution


def test_load_transactions_json():
    # Подготовка
    filename = "test.json"
    expected_data = {
        "key1": "value1",
        "key2": "value2"
    }
    # Запись тестового файла
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(expected_data, f)
    # Выполнение теста
    data = load_transactions_json(filename)
    # Проверка результата
    assert data == expected_data


def test_date_convert():
    # Подготовка данных для теста
    date_time = "2023-05-25T12:34:56.789"
    # Выполнение функции, которую мы тестируем
    result = date_convert(date_time)
    # Проверка ожидаемого поведения
    assert result == "25.05.2023"


def test_sorted_operations_list():
    # Образец операцй
    operations_list = [
        {"date": "2023-05-01", "state": "EXECUTED"},
        {"date": "2023-05-03", "state": "CANCELED"},
        {"date": "2023-05-02", "state": "EXECUTED"},
        {"date": "2023-05-04", "state": "EXECUTED"},
        {"date": "2023-05-05"}  # Отсуствует ключ state
    ]
    # Вызов функции
    result = sorted_operations_list(operations_list)
    # Ожидаемый результат
    assert len(result) == 3
    # Должны быть выполнены только 3 оперции т.к. одна не прошла, в другой нет ключа
    assert result[0]["date"] == "2023-05-04"
    assert result[1]["date"] == "2023-05-02"
    assert result[2]["date"] == "2023-05-01"


def test_card_number_send_from_hide():
    # Подготовка данных для теста
    card_number1 = "Visa Classic 2842878893689012"
    card_number2 = "MasterCard 35158586384610753655"
    card_number3 = "8665240839126074"
    card_number4 = None
    # Проверка ожидаемого поведения
    assert card_number_send_from_hide(card_number1) == "Visa Classic 2842 87** **** 9012"
    assert card_number_send_from_hide(card_number2) == "MasterCard 3515 85** **** 3655"
    assert card_number_send_from_hide(card_number3) == "8665 24** **** 6074"
    assert card_number_send_from_hide(card_number4) == "Отсутствует"


def test_card_number_send_to_hide():
    # Проверка ожидаемого поведения
    card_number = "Maestro 3000704277834087"
    assert card_number_send_to_hide(card_number) == "Maestro **4087"


def test_operations_execution():
    operation = [
        {
            "id": 15948212,
            "state": "EXECUTED",
            "date": "2018-12-23T11:47:52.403285",
            "operationAmount": {
                "amount": "47408.20",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "8665240839126074",
            "to": "Maestro 3000704277834087"
        }
    ]

    assert operations_execution(operation) is None
# Я не смог понять как правильно протестировать эту функцию
# т.к. operations_execution, ничего не возращает, а сразу выводит принт
