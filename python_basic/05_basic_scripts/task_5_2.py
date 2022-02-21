# -*- coding: utf-8 -*-
'''
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

network = input('Введите подсеть в формате x.x.x.x/y: ')

network_list = network.split('/')

ip = network_list[0].split('.')

oct1, oct2, oct3, oct4 = ip[0], ip[1], ip[2], ip[3]

oct1 = int(oct1)

oct2 = int(oct2)

oct3 = int(oct3)

oct4 = int(oct4)

mask = int(network_list[1])

ip_template = '''
...: Network
...: {0:<8} {1:<8} {2:<8} {3:<8}
...: {0:08b} {1:08b} {2:08b} {3:08b}
...: '''

print(ip_template.format(oct1,oct2,oct3,oct4))

mask_full = 32 - mask

mask = str("1" * mask + "0" * mask_full)

mask1 = int(mask[0:8], 2)

mask2 = int(mask[8:16], 2)

mask3 = int(mask[16:24], 2)

mask4 = int(mask[24:33], 2)

mask_template = '''
...: Mask
...: {0:<8} {1:<8} {2:<8} {3:<8}
...: {0:08b} {1:08b} {2:08b} {3:08b}
...: '''

print(mask_template.format(mask1,mask2,mask3,mask4)) 

