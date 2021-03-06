# -*- coding: utf-8 -*-
'''
Задание 12.3


Создать функцию print_ip_table, которая отображает таблицу доступных и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

Функция не должна изменять списки, которые переданы ей как аргументы.
То есть, до выполнения функции и после списки должны выглядеть одинаково.


Для этого задания нет тестов
'''

#from tabulate import tabulate

import tabulate

def print_ip_table(reach, unreach):
	dict = {}
	dict['Reachable:'] = reach
	dict['Unreachable'] = unreach
	print(tabulate.tabulate((dict), headers='keys'))

__name__ = "__main__"

reach = ['192.168.1.1', '192.168.1.23']

unreach = ['159.0.0.0', '345.3.5.6']

print_ip_table(reach, unreach)

