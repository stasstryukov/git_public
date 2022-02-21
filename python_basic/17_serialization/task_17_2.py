# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv), в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы:
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""

import glob
import re
import csv
import os.path

sh_version_files = glob.glob("sh_vers*")
# print(sh_version_files)

headers = ["hostname", "ios", "image", "uptime"]

def parse_sh_version(text_file):
	regex = (r'Cisco .+?, Version (?P<ios>\S+)\,.+\n'
		r'.+\n*.*\n*.*\n*.*\n*.*\n*.*\n*'
		r'.+uptime is (?P<time>.+)\n'
		r'.+\n.+is \"(?P<image>.+)\"')
	match = re.findall(regex, text_file)
	return match

def write_inventory_to_csv(dev_name,result_set,headers):
	output = []
	dev_name_list = []
	dev_param_list = []
	headers = [headers]
	dev_name_list.append(name)
	for param in result_set:
		ios,uptime,image = param
	dev_param_list.append(ios)
	dev_param_list.append(image)
	dev_param_list.append(uptime)
	output.append(dev_name_list + dev_param_list)
	check_file = os.path.isfile('newdata.csv')
	if check_file is False:
		with open('newdata.csv','a') as csv_file:
			writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
			for row in headers:
				writer.writerow(row)
	with open('newdata.csv','a') as file:
			writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
			for row in output:
				writer.writerow(row)


for filename in sh_version_files:
	with open(filename) as f:
		string = f.read()
		result = parse_sh_version(string)
		regex_name = (r'\w+_(?P<name>\w+).+')
		match = re.search(regex_name, filename)
		name = match.group(1)
		write_inventory_to_csv(name,result,headers)
