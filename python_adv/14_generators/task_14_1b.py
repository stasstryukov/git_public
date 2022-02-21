# -*- coding: utf-8 -*-
"""
Задание 14.1b

Создать генератор get_intf_ip_from_files, который ожидает как аргумент
произвольное количество файлов с конфигурацией устройств и возвращает интерсейсы и IP-адреса,
которые настроены на интерфейсах.

Генератор должен обрабатывать конфигурацию и возвращать словарь
для каждого файла на каждой итерации:

* ключ - hostname (надо получить из конфигурационного файла из строки hostname ...)
* значение словарь, в котором:
    * ключ - имя интерфейса
    * значение - кортеж с IP-адресом и маской

Например: {'r1': {'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
                  'FastEthernet0/2': ('10.0.2.2', '255.255.255.0')}}

Проверить работу генератора на примере конфигураций config_r1.txt и config_r2.txt.

"""


import re

def get_intf_ip_from_files(*filenames):
    for filename in filenames:
        result = {}
        with open(filename) as f:
             for line in f:
                 match_device = re.match(r"hostname (?P<dev_name>\S+)",line)
                 if match_device:
                    dev_name = match_device.group(1)
                    result[dev_name] = {}
                 match_iface = re.search(f"^interface (?P<iface>\S+)", line)
                 if match_iface:
                    iface = match_iface.group(1)
                 match_params = re.search(f".*ip address (?P<ip>\S+) (?P<mask>\S+)", line)
                 if match_params:
                    params = match_params.group(1,2)
                    result[dev_name][iface] = params
             yield result

