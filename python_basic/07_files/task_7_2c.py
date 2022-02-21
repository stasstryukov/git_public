# -*- coding: utf-8 -*-
'''
Задание 7.2c

Переделать скрипт из задания 7.2b:
* передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

Внутри, скрипт должен отфильтровать те строки, в исходном файле конфигурации,
в которых содержатся слова из списка ignore.
И записать остальные строки в итоговый файл.

Проверить работу скрипта на примере файла config_sw1.txt.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ignore = ['duplex', 'alias', 'Current configuration']

from sys import argv

file = argv[1]

file_new = argv[2]

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

w = open(file_new,'w')
w.writelines(cfg)
w.close

