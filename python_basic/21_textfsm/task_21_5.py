# -*- coding: utf-8 -*-
"""
Задание 21.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в параллельных потоках функцию send_and_parse_show_command из задания 21.4.

В этом задании надо самостоятельно решить:
* какие параметры будут у функции
* что она будет возвращать


Теста для этого задания нет.
"""

import os
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from task_21_4 import send_and_parse_show_command

def send_and_parse_command_parallel(devices, command, path):
	result = []
	with ThreadPoolExecutor(max_workers=3) as executor:
		future_list = []
		for device in devices:
			future = executor.submit(send_and_parse_show_command, device, command, path)
			future_list.append(future)
	for future in as_completed(future_list):
		result.append(future.result())
	return result

if __name__ == "__main__":
	path = os.path.abspath('templates')
	with open("devices.yaml") as f:
		devices = yaml.safe_load(f)
	command = "sh ip int br"
	result = send_and_parse_command_parallel(devices, command, path)
	print(result)
