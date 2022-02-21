# -*- coding: utf-8 -*-
'''
Задание 5.2a

Всё, как в задании 5.2, но, если пользователь ввел адрес хоста, а не адрес сети,
надо преобразовать адрес хоста в адрес сети и вывести адрес сети и маску, как в задании 5.2.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.1/30 - хост из сети 10.0.5.0/30

Если пользователь ввел адрес 10.0.1.1/24,
вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

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

mask = int(network_list[1])

end_mask = 32 - mask

oct1, oct2, oct3, oct4 = int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3])

oct1 = '{:08b}'.format(oct1)

oct2 = '{:08b}'.format(oct2)

oct3 = '{:08b}'.format(oct3)

oct4 = '{:08b}'.format(oct4)

print(oct1)
print(oct2)
print(oct3)
print(oct4)

oct = oct1+oct2+oct3+oct4

oct = oct.replace('0b','')

oct = oct[0:mask]

oct = oct + '0' * end_mask

oct1 = int(oct[0:8], 2)

oct2 = int(oct[8:16], 2)

oct3 = int(oct[16:24], 2)

oct4 = int(oct[24:33], 2)

ip_template = '''
...: Network
...: {0:<8} {1:<8} {2:<8} {3:<8}
...: {0:08b} {1:08b} {2:08b} {3:08b}
...: '''

print(ip_template.format(oct1,oct2,oct3,oct4))


mask = str("1" * mask + "0" * end_mask)

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
