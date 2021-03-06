# -*- coding: utf-8 -*-
"""
Задание 8.4a

Переделать декоратор retry из задания 8.4: добавить параметр delay,
который контролирует через какое количество секунд будет выполняться повторная попытка.
При каждом повторном запуске результат проверяется:

* если он был истинным, он возвращается
* если нет, функция запускается повторно заданное количество раз

Пример работы декоратора:
In [2]: @retry(times=3, delay=5)
    ..: def send_show_command(device, show_command):
    ..:     print('Подключаюсь к', device['ip'])
    ..:     try:
    ..:         with ConnectHandler(**device) as ssh:
    ..:             ssh.enable()
    ..:             result = ssh.send_command(show_command)
    ..:         return result
    ..:     except (NetMikoAuthenticationException, NetMikoTimeoutException):
    ..:         return None
    ..:

In [3]: send_show_command(device_params, 'sh clock')
Подключаюсь к 192.168.100.1
Out[4]: '*16:35:59.723 UTC Fri Oct 18 2019'

In [5]: device_params['password'] = '123123'

In [6]: send_show_command(device_params, 'sh clock')
Подключаюсь к 192.168.100.1
Повторное подключение через 5 сек
Подключаюсь к 192.168.100.1
Повторное подключение через 5 сек
Подключаюсь к 192.168.100.1
Повторное подключение через 5 сек
Подключаюсь к 192.168.100.1


Тест берет значения из словаря device_params в этом файле, поэтому если
для заданий используются другие адреса/логины, надо заменить их в словаре.
"""

from netmiko import (
    ConnectHandler,
    NetMikoAuthenticationException,
    NetMikoTimeoutException,
)
import time

device_params = {
    "device_type": "cisco_ios",
    "ip": "10.0.14.100",
    "username": "stasstr",
    "password": "Gjkzhyjtcbzybt1",
}


def retry(times, delay):
    times +=2
    def decorator(func):
        def inner(*args, **kwargs):
            check = None
            while check == None:
                for num in range(times):
                    if num == times-1:
                        return ""
                    elif num != times:
                        result = func(*args, **kwargs)
                        if result != None:
                           check = 1
                           return result
                        elif (result == None) and (num < times-2):
                           print(f"Повторное подключение через {delay} сек")
                           time.sleep(delay)
                        else: pass
        return inner
    return decorator


@retry(times=3, delay=1)
def send_show_command(device, show_command):
    print("Подключаюсь к", device["ip"])
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(show_command)
        return result
    except (NetMikoAuthenticationException, NetMikoTimeoutException):
        return None


if __name__ == "__main__":
    output = (send_show_command(device_params, "sh clock"))
    print(output)
