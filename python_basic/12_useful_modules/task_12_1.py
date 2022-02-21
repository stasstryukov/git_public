# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

import subprocess

def ping_ip_addresses(ip):
	result = subprocess.run(['ping', '-c', '2', '-n', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	if result.returncode == 0:
		return True
	else: return False

__name__ = "__main__"

ip_list = ['8.8.8.8', '192.168.1.21', '267.0.3.2']

avail_ip = []
notavail_ip = []

for ip in ip_list:
	result = ping_ip_addresses(ip)
	if result == True:
		avail_ip.append(ip)
	else: notavail_ip.append(ip)

print(tuple(avail_ip))
print(tuple(notavail_ip))
