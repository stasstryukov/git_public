# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""

import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import repeat
import netmiko


def show_ip(device, command):
	with netmiko.ConnectHandler(**device) as ssh:
		ssh.enable()
		command_out = ssh.send_command(command)
		prompt = ssh.find_prompt()
		result = prompt + command + '\n' + command_out 
		return result

def send_show_command_to_devices(devices, command = 'sh ip int br', filename = 'result.txt', limit=3):
	with ThreadPoolExecutor(max_workers=limit) as executor:
		result = executor.map(show_ip, devices, repeat(command))
		for device, output in zip(devices, result):
			with open(filename,'a') as file:
				file.write(output + '\n')

if __name__ == "__main__":

	with open('devices.yaml') as f:
        	devices = yaml.safe_load(f)

	send_show_command_to_devices(devices)

