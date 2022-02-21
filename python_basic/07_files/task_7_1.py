# -*- coding: utf-8 -*-
'''
Задание 7.1

Аналогично заданию 4.6 обработать строки из файла ospf.txt
и вывести информацию по каждой в таком виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

f = open('ospf.txt', 'r')

for line in f:
	print('\n')
	line = line.replace('O ', 'OSPF')
	line = line.replace(',', '')
	ospf = line.split()
	ospf[2] = ospf[2].strip('[]');
	print('Protocol: ' + ospf[0])
	print('Prefix: ' + ospf[1])
	print('AD/Metric: ' + ospf[2])
	print('Next-Hop: ' + ospf[4])
	print('Last update: ' + ospf[5])
	print('Outbound Interface: ' + ospf[6])

f.close()
