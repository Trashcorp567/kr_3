# Загрузаем нужные функции из файла func.py
from func import load_transactions_json, operations_execution, sorted_operations_list

# Основной код программы, который работает на основе написанных функий

# operations_list - служит для активации функции чтения файла из json
operations_list = load_transactions_json("operations.json")

# sorted_list - используется для сортировки данных по времени и срезе последних 5 операций
sorted_list = sorted_operations_list(operations_list)

# operations_execution - функция, которая выводит информацию на основе отсортированного списка
operations_execution(sorted_list)