# -*- coding: utf-8 -*-
'''
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Дополнить скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

vlan_sel = input('Введите VLAN: ')

lines = []
with open('CAM_table.txt', 'r') as f:
  for line in f:
    if line.count('.') == 2:
      vlan, mac, _, intf = line.rstrip().split()
      lineList = [int(vlan), mac, intf]
      lines.append(lineList)
for line in lines:
  if line[0] == int(vlan_sel):
    print('{:<5}  {}    {}'.format(line[0], line[1], line[2]))

