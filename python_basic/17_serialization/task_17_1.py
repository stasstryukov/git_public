# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает
вывод команды show dhcp snooping binding из разных файлов и записывает обработанные данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21


Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.
Первый столбец в csv файле имя коммутатора надо получить из имени файла, остальные - из содержимого в файлах.

"""

import re
import csv
import os.path

def write_dhcp_snooping_to_csv(file):
	output = []
	regex = (r'(?P<mac>\S+) +(?P<ip>\S+) +\d+ +\S+ +(?P<vlan>\d+) +(?P<intf>\S+)')
	name = file.split('_')
	name = name[0]
	with open(file) as f:
		for line in f:
			match = re.search(regex,line)
			if match:
				headers = [["switch", "mac", "ip", "vlan", "interface"]]
				check_file = os.path.isfile('output.csv')
				if check_file is False:
					with open('output.csv','a') as csv_file:
                                       		writer = csv.writer(csv_file)
                                       		for row in headers:
                                               		writer.writerow(row)
				dev_name = []
				dev_param = []
				dev_name.append(name)
				dev_param = list(match.groups())
				output.append(dev_name + dev_param)
				with open('output.csv','a') as csv_file:
					writer = csv.writer(csv_file)
					for row in output:
						writer.writerow(row)

files = input('Введите имена файлов через запятую: ')

files = files.split(',')

for filename in files:
	filename = filename.replace(' ', '')
	write_dhcp_snooping_to_csv(filename)
