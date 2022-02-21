# -*- coding: utf-8 -*-
'''
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'

ospf_route = ospf_route.replace('O ', 'OSPF')

ospf_route = ospf_route.replace ('[110/41]', '110/41')

ospf = ospf_route.split()

print('Protocol: ' + ospf[0])
print('Prefix: ' + ospf[1])
print('AD/Metric: ' + ospf[2])
print('Next-Hop: ' + ospf[4])
print('Last update: ' + ospf[5])
print('Outbound Interface: ' + ospf[6])

