# -*- coding: utf-8 -*-
"""
Задание 14.2

Создать генератор read_file_in_chunks, который считывает файл по несколько строк.

Генератор ожидает как аргумент имя файла и количество строк, которые нужно считать за раз
и должен возвращать указанное количество строк одной строкой на каждой итерации.
Строки файла должны считываться по необходимости, то есть нельзя считывать все строки файла за раз.

Параметры функции:

* filename - имя файла из которого считываются строки
* chunk_size - сколько строк считывать за раз

Проверить работу генератора на примере файла config_r1.txt.

Убедиться, что все строки возвращаются. Если в последней итерации строк меньше, чем указано в chunk_size,
они всё равно должны возвращаться. После того как строки закончились, генератор должен останавливаться.

Ограничение: нельзя использовать функции из модуля itertools.

Пример использования функции:
In [1]: g = read_file_in_chunks('config_r1.txt', 10)

In [2]: next(g)
Out[2]: 'Current configuration : 4052 bytes\n!\n! Last configuration change at 13:13:40 UTC Tue Mar 1 2016\nversion 15.2\nno service timestamps debug uptime\nno service timestamps log uptime\nno service password-encryption\n!\nhostname PE_r1\n!\n'

"""


def read_file_in_chunks(filename, chunk_size):
    with open(filename) as f:
        line = ''
        for line in f:
            count = 1
            result = line
            while count < chunk_size:
                line = f.readline()
                result +=line
                count += 1
            yield result
            if not line:
                return
