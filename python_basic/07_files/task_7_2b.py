# -*- coding: utf-8 -*-
'''
Задание 7.2b

Дополнить скрипт из задания 7.2a:
* вместо вывода на стандартный поток вывода,
  скрипт должен записать полученные строки в файл config_sw1_cleared.txt

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore.
Строки, которые начинаются на '!' отфильтровывать не нужно.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

from sys import argv

file = argv[1]

cfg = []

with open(file, 'r') as f:
        for line in f:
                        for bad in ignore:
                                bool = True
                                if line.find(bad) == -1:
                                        bool = True
                                else:
                                        bool = False
                                        break
                        if bool is True:
                                cfg.append(line.rstrip() + '\n')

w = open('config_sw1_cleared.txt','w')
w.writelines(cfg)
w.close


