# -*- coding: utf-8 -*-
"""
Задание 4.3

Написать тест(ы), который проверяет есть ли маршрут 192.168.100.0/24 в таблице
маршрутизации (команда sh ip route) на маршрутизаторах, которые указаны в файле devices.yaml.

Для проверки надо подключиться к каждому маршрутизатору с помощью netmiko
и проверить маршрут командой sh ip route или разновидностью команды sh ip route.

Тест(ы) должен проходить, если маршрут есть.
Тест может быть один или несколько.

Тест(ы) написать в файле задания.
"""

import pytest
import yaml
from netmiko import ConnectHandler


with open('devices.yaml') as f:
   devices = yaml.safe_load(f)

@pytest.fixture(params=devices, scope="session",)
def find_route(request):
#    for device in devices_params:
   ssh = ConnectHandler(**request.param)
   ssh.enable()
   yield ssh
   ssh.disconnect()

@pytest.mark.parametrize( 'route',["192.168.88.0"])
def test_find_route(find_route, route):
    result = find_route.send_command("sh ip route | in 192.168.88.0")
    assert "192.168.88.0" in result
       




            
