# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

import re

def parse_sh_cdp_neighbors(configline):
	regex = (r'(?P<our_name>\S+)>'
		r'|(?P<our_port>\S+ \d+[\/]\d+)'
		r'|\n(?P<nei_name>\S+)\s{2,}'
		r'|\d+.+ (?P<nei_port>\S+ \d+\/\d+)')
	match_iter = re.finditer(regex,configline)
	result = {}
	for match in match_iter:
		if match.lastgroup == 'our_name':
			our_name = match.group(match.lastgroup)
			result[our_name] = {}
		elif match.lastgroup == 'our_port':
			our_port = match.group(match.lastgroup)
			result[our_name][our_port] = {}
		elif match.lastgroup == 'nei_name':
			nei_name = match.group(match.lastgroup)
			nei = {}
			nei[nei_name] = {}
		elif match.lastgroup == 'nei_port':
			nei[nei_name] = match.group(match.lastgroup)
			result[our_name][our_port] = nei
	return result

filename = input('Введите название файла: ')

f = open(filename)
line = f.read()
f.close()
result = parse_sh_cdp_neighbors(line)
print(result)
