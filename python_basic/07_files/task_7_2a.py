# -*- coding: utf-8 -*-
'''
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

from sys import argv

file = argv[1]

with open(file, 'r') as f:
	for line in f:
		if line.startswith('!') is False:
			for bad in ignore:
				bool = True
				if line.find(bad) == -1:
	                       		bool = True
				else:
					bool = False
					break
			if bool is True:
				print(line.strip())
		else:
			continue


