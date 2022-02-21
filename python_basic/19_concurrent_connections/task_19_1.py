# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""

import subprocess
from concurrent.futures import ThreadPoolExecutor

def ping_ip_address(ip):
	ping = subprocess.run(['ping', '-c', '5', '-n', ip], stdout=subprocess.DEVNULL)
	if ping.returncode == 0:
		return True

def ping_ip_addresses(ip_list, limit = 3):
	reach = []
	unreach = []
	with ThreadPoolExecutor(max_workers=limit) as executor:
		results = executor.map(ping_ip_address, ip_list)
		for ip, alive in zip(ip_list, results):
#			print(ip,alive)
			if alive is True:
				reach.append(ip)
			else: unreach.append(ip)
	return reach, unreach

if __name__ == "__main__":
	print(ping_ip_addresses(["8.8.8.8", "8.8.4.4", "10.150.1.1"]))

