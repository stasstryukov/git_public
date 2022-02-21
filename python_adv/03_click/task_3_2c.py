# -*- coding: utf-8 -*-
"""
Задание 3.2c

Скопировать функцию cli и настройку click из задания 3.2a или 3.2b.
Добавить отображение progress bar при выполнении скрипта. Для этого можно менять функцию send_command_to_devices. При этом функция по-прежнему должна выполнять подключение в потоках.

Пример вызова:
$ python task_3_2c.py "sh clock" 192.168.100.1 192.168.100.2 192.168.100.3 -u cisco -p cisco -s cisco -t 1
Connecting to devices  [####################################]  100%
['sh clock\r\n*08:35:15.963 UTC Fri Sep 11 2020\r\nR1#',
 'sh clock\r\n*08:35:17.025 UTC Fri Sep 11 2020\r\nR2#',
 'sh clock\r\n*08:35:18.087 UTC Fri Sep 11 2020\r\nR3#']

Для этого задания нет теста!
"""

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
import yaml
from cisco_telnet_class import CiscoTelnet
from netmiko import ConnectHandler
import click


def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
          output = ssh.send_command(command)
    return output


def send_command_to_devices(devices, command, threads=5):
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
       futures = [
             executor.submit(send_show_command, device, command) for device in devices
       ]
       with click.progressbar(length=len(futures), label="Подключаемся к устройствам") as bar:
              for future in as_completed(futures):
                   results.append(future.result())
                   bar.update(1)
    return results


# Это просто заготовка, чтобы не забыть, что click надо применять к этой функции

@click.command()
@click.argument("command")
@click.argument("ip_list", nargs=-1)
@click.option("--username","-u", required=True,prompt=True)
@click.option("--password","-p", required=True,prompt=True,hide_input=True)
@click.option("--threads","-t", type=click.IntRange(1,10),default=5)
@click.option("--timed", is_flag = True)
def cli(command,ip_list,username,password,threads,timed):
    start_time = datetime.now()
    devices = []
    for ip in ip_list:
        device = {}
        device["device_type"] = "cisco_ios"
        device["ip"] = ip
        device["username"] = username
        device["password"] = password
        devices.append(device)
    pprint(send_command_to_devices(devices, command, threads))


if __name__ == "__main__":
    cli()
