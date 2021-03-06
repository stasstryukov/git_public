# -*- coding: utf-8 -*-
"""
Задание 12.3a

Скопировать класс Topology из задания 12.3.
Переделать класс Topology таким образом, чтобы абстрактные методы
могли удалять соединение и в том случае, когда вместо ключа, передается
значение из словаря.


При создании экземпляра класса, как аргумент теперь передается словарь,
который может содержать дублирующиеся соединения.

Дублем считается ситуация, когда в словаре есть такие пары:
('R1', 'Eth0/0'): ('SW1', 'Eth0/1') и ('SW1', 'Eth0/1'): ('R1', 'Eth0/0')

При создании экземпляра класса надо удалить дубли и записать словарь без дублей в переменную
topology. При удалении дублей надо оставить ту пару, где key < value.

То есть ключом должно быть меньший кортеж, а значением больший.
Из таким двух пар:
('R1', 'Eth0/0'): ('SW1', 'Eth0/1') и ('SW1', 'Eth0/1'): ('R1', 'Eth0/0')

должна остаться первая
('R1', 'Eth0/0'): ('SW1', 'Eth0/1').

Пример создания экземпляра класса:
In [1]: t1 = Topology(example1)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка реализации абстрактных методов:

получение элемента:
In [3]: t1[('R1', 'Eth0/0')]
Out[3]: ('SW1', 'Eth0/1')

In [4]: t1[('SW1', 'Eth0/2')]
Out[4]: ('R2', 'Eth0/0')

Перезапись/запись элемента:
In [5]: t1[('R1', 'Eth0/0')] = ('SW1', 'Eth0/12')

In [6]: t1.topology
Out[6]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [7]: t1[('R6', 'Eth0/0')] = ('SW1', 'Eth0/17')

In [8]: t1.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
 ('R6', 'Eth0/0'): ('SW1', 'Eth0/17')}

In [9]: t1[('SW1', 'Eth0/21')] = ('R7', 'Eth0/0')

In [10]: t1.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
 ('R6', 'Eth0/0'): ('SW1', 'Eth0/17'),
 ('R7', 'Eth0/0'): ('SW1', 'Eth0/21')}

Удаление:
In [11]: del t1[('R7', 'Eth0/0')]

In [12]: t1.topology
Out[12]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
 ('R6', 'Eth0/0'): ('SW1', 'Eth0/17')}

In [13]: del t1[('SW1', 'Eth0/17')]

In [14]: t1.topology
Out[14]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Итерация:
In [15]: for item in t1:
    ...:     print(item)
    ...:
('R1', 'Eth0/0')
('R2', 'Eth0/0')
('R2', 'Eth0/1')
('R3', 'Eth0/0')
('R3', 'Eth0/1')
('R3', 'Eth0/2')

Длина:
In [16]: len(t1)
Out[16]: 6

"""

example1 = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R4", "Eth0/0"): ("R3", "Eth0/1"),
    ("R5", "Eth0/0"): ("R3", "Eth0/2"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

example2 = {("R1", "Eth0/4"): ("R7", "Eth0/0"), ("R1", "Eth0/6"): ("R9", "Eth0/0")}

from collections.abc import MutableMapping

class Topology(MutableMapping):
      def __init__(self, topology):
          self.topology = topology
          duplicate = []
          for key,value in self.topology.items():
              for item in self.topology.values():
                  if key == item:
                     if (value[0] < item[0]) & (key not in duplicate):
                        duplicate.append(key)
          for item in duplicate:
              del self.topology[item]


      def __setitem__(self, key, value):
          self.topology[key] = value

      def __getitem__(self, key):
          try:
              return self.topology[key]
          except KeyError:
              for temp_key, temp_value in self.topology.items():
                  if temp_value == key:
                     return temp_key

      def __delitem__(self, key):
          try:
              del self.topology[key]
          except KeyError:
              temp_topology = self.topology.copy()
              for temp_key, temp_value in temp_topology.items():
                  if temp_value == key:
                      del self.topology[temp_key]

      def __iter__(self):
          return iter(self.topology)

      def __len__(self):
          return len(self.topology)

