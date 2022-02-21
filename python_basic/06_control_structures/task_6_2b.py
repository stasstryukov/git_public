# -*- coding: utf-8 -*-
'''
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт:
Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ip_correct = False

while not ip_correct:
	ip = input('Введите ip: ')
	ip_list = ip.split('.')
	check = 1
	for ip_str in ip_list:
        	if ip_str.isdigit() == True:
                	if int(ip_str) >= 0 and int(ip_str) <= 255 and check != 2:
                        	check = 1
                	else:
                        	check = 2
                        	break
        	else:
                	check = 2
                	break

	if check != 2:
		ip_correct = True
		ip1 = int(ip_list[0])
		if ip1 >= 1 and ip1 <= 223:
			print('unicast')
		elif ip1 >= 224 and ip1 <= 239:
			print('multicast')
		elif ip == '255.255.255.255':
			print('local broadcast')
		elif ip == '0.0.0.0':
			print('unassigned')
		else: print('unused')
	else:
        	print('Неправильный IP-адрес')

