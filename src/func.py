import json
from datetime import datetime


def load_transactions_json(filename):
    """
    Конвертирует json файл и кодирует его в utf-8
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def sorted_operations_list(operations_list):
    """
    Сортирует исходный список на основе значения даты, а так же по выполнению оперции
    key=lambda x: x.get("date", "") - используется в случае если, информация о
    выполении операции отсутствует, после чего сортирует их в порядке убывания временного
    промежутка
    P.s. Пришлось гуглить решение: через базовый поиск по ключу, выдаёт ошибку,
    Насколько я понял, не во всех операция присутствует ключ state, проверить глазами - неудалось
    За то, я научился пользоваться методом get
    """
    executed_operations = [operation for operation in operations_list if operation.get("state") == "EXECUTED"]
    sorted_by_date_list = sorted(executed_operations, key=lambda x: x.get("date", ""), reverse=True)
    return sorted_by_date_list[:5]


def date_convert(date_time):
    """
    Конвертирует дату операций в фомат ДД.ММ.ГГГГ
    """
    date_time_conv = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
    return date_time_conv


def card_number_send_from_hide(card_number):
    """
    Скрывает номер карты или счёта отправителя
    и выводит в формате:
    Счёт/карта XXXX XX** **** XXXX
    Если данные об отправке отсутствует, делает проверку на значение "from"
    И возвращет "Отсутствует" чтобы избежать падений программы
    """
    if card_number is not None and card_number.count(" ") >= 2:
        split_number = card_number.split(" ")
        last_four_digits = split_number[2]
        masked_number = f"{split_number[0]} {split_number[1]} " \
                        f"{last_four_digits[:4]} {last_four_digits[4:6]}** **** {last_four_digits[-4:]}"
        return masked_number
    elif card_number is not None and card_number.count(" ") == 1:
        split_number = card_number.split(" ")
        card_type = split_number[0]
        last_four_digits = split_number[-1]
        masked_number = f"{card_type} {last_four_digits[:4]} {last_four_digits[4:6]}** **** {last_four_digits[-4:]}"
        return masked_number
    else:
        last_four_digits = card_number
        if last_four_digits is not None:
            masked_number = f"{last_four_digits[:4]} {last_four_digits[4:6]}** **** {last_four_digits[-4:]}"
            return masked_number
        else:
            return "Отсутствует "


def card_number_send_to_hide(card_number):
    """
    Скрывает номер карты или счёта получателя
    и выводит только тип карты и последние 4 цифры, остальное, скрыто
    """
    split_number = card_number.split(" ")
    card_type = split_number[0]
    last_four_digits = split_number[1]
    masked_number = f"{card_type} **{last_four_digits[-4:]}"
    return masked_number


def operations_execution(operation):
    """
    Функция выводит последние 5 оперций в отформатированном ввиде
    на основе функций написанных выше
    """
    for item in operation:
        date = date_convert(item["date"])
        description = item["description"]
        operation = item["operationAmount"]["amount"]
        operation_currency = item["operationAmount"]["currency"]["name"]
        send_from = card_number_send_from_hide(item.get("from"))
        send_to = card_number_send_to_hide(item["to"])
        print(f"{date} {description}\n" 
              f"{send_from} -> {send_to}\n"
              f"{operation} {operation_currency}\n")
