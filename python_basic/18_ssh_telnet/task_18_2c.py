# -*- coding: utf-8 -*-
"""
Задание 18.2c

Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка,
спросить пользователя надо ли выполнять остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию, поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

"""

from netmiko import ConnectHandler
import yaml
import re
from pprint import pprint

# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]

commands = commands_with_errors + correct_commands

def send_config_commands(device, commands, log='False'):
        good_comm = {}
        bad_comm = {}
        regex = "% (?P<errormsg>).+"
        if log == 'True':
                print(f"Подключаюсь к {device['host']}")
        with ConnectHandler(**device) as ssh:
                ssh.enable()
                for command in commands:
                        result = ssh.send_config_set(command, exit_config_mode=False)
                        match = re.search(regex, result)
                        if match:
                                error = match.group("errormsg")
                                print('*'*30)
                                print(f"Комманда {command} завершилась с ошибкой {error} на устройстве {device['host']}")
                                print('*'*30)
                                bad_comm[command] = result
                                contin = input('Выполнять дальше? y/n: ')
                                if contin == 'n' or contin == 'no':
                                    break
                        else: good_comm[command] = result
                ssh.exit_config_mode()
        return good_comm, bad_comm

if __name__ == "__main__":
        with open("devices.yaml") as f:
                devices = yaml.safe_load(f)
        for device in devices:
                log = input('Нужен лог? True/False(по умолчанию False): ')
                pprint(send_config_commands(device, commands, log))

