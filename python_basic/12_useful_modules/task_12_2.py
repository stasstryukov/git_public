# -*- coding: utf-8 -*-
'''
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона, например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список, где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список IP-адресов и/или диапазонов IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только последний октет адреса.

Функция возвращает список IP-адресов.


Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

'''

import ipaddress

def convert_ranges_to_ip_list(ip):
	ip_list = []
	try:
		ipaddress.ip_network(ip)
		return True
	except ValueError:
		ip = ip.split('-')
		ip1,ip2,ip3, *other = ip[0].split('.')
		if '.' in ip[1]:
			ip_first = ipaddress.ip_address(ip[0])
			ip_last = ipaddress.ip_address(ip[1])
			while ip_first <= ip_last:
				ip_list.append(str(ip_first))
				ip_first += 1
		elif '.' not in ip[1]:
			ip_last = ip1 + '.' + ip2 + '.' + ip3 + '.' + ip[1]
			ip_first = ipaddress.ip_address(ip[0])
			ip_last = ipaddress.ip_address(ip_last)
			while ip_first <= ip_last:
				ip_list.append(str(ip_first))
				ip_first += 1
		return ip_list

__main__ = "__name__"

iplist = ['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

unpacked = []

for ip in iplist:
	result = convert_ranges_to_ip_list(ip) 
	if result == True:
		unpacked.append(ip)
	else: unpacked.extend(result)

print(unpacked)
