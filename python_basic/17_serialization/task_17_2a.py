# -*- coding: utf-8 -*-
'''
Задание 17.2a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод команды show cdp neighbor из нескольких файлов и записывает итоговую топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами, независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь в файл topology.yaml.

'''


import yaml
import re
import glob

def generate_topology_from_cdp(list_of_files,save_to_filename=None):
	dict = {}
	for filename in list_of_files:
		our_name = re.search(r"sh_cdp_n_(?P<name>\w+).txt", filename).group(1)
		our_name = our_name.upper()
		dict[our_name] = {}
		regex = ('(?P<nei_name>\S+) +(?P<our_port>\S+ \S+).+ (?P<nei_port>\S+ \w+\/\w+)')
		with open(filename) as f:
			for line in f:
				match = re.match(regex,line)
				if match:
					nei_name, our_port, nei_port = match.group("nei_name","our_port","nei_port")
					dict[our_name][our_port] = {nei_name: nei_port}
	if save_to_filename:
		with open(save_to_filename, 'w') as file_yaml:
			yaml.dump(dict,file_yaml, default_flow_style=False)
	return dict


if __name__ == "__main__":
	f_list = glob.glob("sh_cdp_n_*")
	print(generate_topology_from_cdp(f_list, save_to_filename = "topology.yaml"))

