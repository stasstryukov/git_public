# -*- coding: utf-8 -*-
'''
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
'''

import re

def get_ints_without_description(conf):
	regex = (r'interface (\S+)\n ip unnumbered'
		r'|interface (\S+)\n no ip'
		r'|interface (\S+)\n ip address')
	result = []
	with open(conf) as f:
		match = re.finditer(regex,f.read(),re.DOTALL)
		for m in match:
			int_match = m.groups()
			for intf in int_match:
				if intf != None:
					result.append(intf)
	return result

result = get_ints_without_description('config_r1.txt')

print(result)
