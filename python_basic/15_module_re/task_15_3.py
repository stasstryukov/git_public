# -*- coding: utf-8 -*-
'''
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
'''

import re

def convert_ios_nat_to_asa(config_start, config_end):
	regex = ('.+ source (?P<type>\D+) (?P<proto>\D+) (?P<ip>.+?) (?P<port_in>\d+) (.+) (.+) (?P<port_out>\d+)')
	template = ['object network LOCAL_{}',
                    ' host {}',
                    ' nat (inside,outside) {} interface service {} {} {}']
	with open(config_start) as cfg:
		for line in cfg:
			match = re.search(regex,line)
			type, proto, ip, port_in, port_out = match.group(1,2,3,4,7)
			cfg_asa_nat = '\n'.join(template).format(ip,ip,type,proto,port_in,port_out)
			f = open(config_end, 'a')
			f.write(cfg_asa_nat + '\n')
			f.close()

startfile = input('Введите имя файла: ')

endfile = input ('Введите имя конечного файла: ')

convert_ios_nat_to_asa(startfile, endfile)

