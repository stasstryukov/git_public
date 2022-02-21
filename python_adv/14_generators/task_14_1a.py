# -*- coding: utf-8 -*-
"""
Задание 14.1a

Создать генератор get_intf_ip, который ожидает как аргумент имя файла,
в котором находится конфигурация устройства и возвращает все интерфейсы и IP-адреса,
которые настроены на интерфейсах.

Генератор должен обрабатывать конфигурацию и возвращать кортеж на каждой итерации:
* первый элемент кортежа - имя интерфейса
* второй элемент кортежа - IP-адрес
* третий элемент кортежа - маска

Например: ('FastEthernet', '10.0.1.1', '255.255.255.0')

Проверить работу генератора на примере файла config_r1.txt.
"""


import re

def get_intf_ip(filename):
    with open(filename) as f:
        for line in f:
            match_iface = re.search(f"^interface (?P<iface>\S+)", line)
            if match_iface:
               result = []
               iface = match_iface.group(1)
               result.append(iface)
            match_params = re.search(f".*ip address (?P<ip>\S+) (?P<mask>\S+)", line)
            if match_params:
               ip, mask = match_params.group(1,2)
               result.append(ip)
               result.append(mask)
               yield tuple(result)

