# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM (templates/sh_ip_int_br.template)
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.
"""

from netmiko import ConnectHandler
import textfsm

def parse_output_to_dict(template, command_output):
	dict = {}
	final = []
	with open(template) as t:
		fsm = textfsm.TextFSM(t)
		header = fsm.header
		result = fsm.ParseText(command_output)
		for list in result:
			for key,value in zip(header,list):
				dict[key] = value
			final.append(dict)
	return final

if __name__ == "__main__":
    r1_params = {
        "device_type": "cisco_ios",
        "host": "192.168.1.101",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with ConnectHandler(**r1_params) as r1:
        r1.enable()
        output = r1.send_command("sh ip int br")
    result = parse_output_to_dict("templates/sh_ip_int_br.template", output)
    print(result)
