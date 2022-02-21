# -*- coding: utf-8 -*-
'''
Задание 11.2

Создать функцию create_network_map, которая обрабатывает
вывод команды show cdp neighbors из нескольких файлов и объединяет его в одну общую топологию.

У функции должен быть один параметр filenames, который ожидает как аргумент список с именами файлов, в которых находится вывод команды show cdp neighbors.

Функция должна возвращать словарь, который описывает соединения между устройствами.
Структура словаря такая же, как в задании 11.1:
    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}


Cгенерировать топологию, которая соответствует выводу из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt

В словаре, который возвращает функция create_network_map, не должно быть дублей.

С помощью функции draw_topology из файла draw_network_graph.py нарисовать схему на основании топологии, полученной с помощью функции create_network_map.
Результат должен выглядеть так же, как схема в файле task_11_2a_topology.svg


При этом:
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме

Не копировать код функций parse_cdp_neighbors и draw_topology.

Ограничение: Все задания надо выполнять используя только пройденные темы.

> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

'''

import draw_network_graph

def create_network_map(config):
	cfg = open(config, 'r')
	for line in cfg:
		if '>' in line:
			our_dev_name = line.split('>')
			our_dev_name = our_dev_name[0]
			break
		else: pass
		if 'Eth' in line:
			line = line.split()
			remote_dev_name = line[0]
			iface_our = line[1] + line[2]
			iface_remote = line[-2] + line[-1]
			our_device = (our_dev_name, iface_our)
			remote_device = (remote_dev_name, iface_remote)
			neighbors_dict[our_device] = remote_device
		else: pass
	return neighbors_dict

config_files = ["sh_cdp_n_sw1.txt", "sh_cdp_n_r1.txt", "sh_cdp_n_r2.txt", "sh_cdp_n_r3.txt"]

neighbors_dict = {}

for file in config_files:
	result = create_network_map(file)

topology_dict = result.copy()

for key, value in result.items():
	if key[0] != 'SW1':
		for value2, key2 in result.items():
			if key == key2:
				del topology_dict[key2]

draw_network_graph.draw_topology(topology_dict)

