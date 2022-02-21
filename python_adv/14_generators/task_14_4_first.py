# -*- coding: utf-8 -*-
"""
Задание 14.4

Переделать код функции send_show_command_to_devices таким образом, чтобы
она была генератором и возвращала вывод с одного устройства на каждой итерации.
Функция send_show_command_to_devices не должна выполнять запись в файл.

Переделать соответственно код, который вызывает send_show_command_to_devices
таким образом, чтобы результат, который генерирует send_show_command_to_devices
записывался в файл.

Проверить работу генератора на устройствах из файла devices.yaml.
Для этого задания нет теста!
"""
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from netmiko import ConnectHandler
import yaml


def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        prompt = ssh.find_prompt()
    return f"{prompt}{command}\n{result}\n"



def send_show_command_to_device(device, command):
        return send_show_command(device, command)

if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    with open("result.txt", "w") as f:
         for device in devices:
             result = send_show_command_to_device(device, command)
#             for line in result:
             print(result)
             f.write(result)







