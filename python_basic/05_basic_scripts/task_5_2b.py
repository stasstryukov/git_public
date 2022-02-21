# -*- coding: utf-8 -*-
'''
Задание 5.2b

Преобразовать скрипт из задания 5.2a таким образом,
чтобы сеть/маска не запрашивались у пользователя,
а передавались как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

from sys import argv

ip = argv[1]

ip = ip.split('.')

mask = int(argv[2])

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
