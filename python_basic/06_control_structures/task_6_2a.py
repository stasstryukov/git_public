# -*- coding: utf-8 -*-
'''
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
'Неправильный IP-адрес'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

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

