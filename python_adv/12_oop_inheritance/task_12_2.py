# -*- coding: utf-8 -*-
"""
Задание 12.2

Скопировать класс IPv4Network из задания 11.1 и изменить его таким
образом, чтобы класс IPv4Network наследовал абстрактный класс Sequence.
Создать все необходимые абстрактные методы для работы IPv4Network как Sequence.

Проверить, что работают все методы характерные для последовательности (sequence):
* __getitem__, __len__, __contains__, __iter__, index, count

Пример создания экземпляра класса:

In [1]: net1 = IPv4Network('8.8.4.0/29')

Проверка методов:

In [2]: len(net1)
Out[2]: 6

In [3]: net1[0]
Out[3]: '8.8.4.1'

In [4]: '8.8.4.1' in net1
Out[4]: True

In [5]: '8.8.4.10' in net1
Out[5]: False

In [6]: net1.count('8.8.4.1')
Out[6]: 1

In [7]: net1.index('8.8.4.1')
Out[7]: 0

In [8]: for ip in net1:
   ...:     print(ip)
   ...:
8.8.4.1
8.8.4.2
8.8.4.3
8.8.4.4
8.8.4.5
8.8.4.6


"""

import ipaddress
from collections.abc import Sequence


class IPv4Network(Sequence):
      def __init__(self, network):
          self.net1 = ipaddress.ip_network(network)
          self._addresses = [str(ip) for ip in self.net1.hosts()]
          self._addresses = tuple(self._addresses)

      def __getitem__(self, index):
          return self._addresses[index]

      def __iter__(self):
          return iter(self._addresses)

      def __len__(self):
          return len(self._addresses)

      def __contains__(self, item):
          return item in self._addresses

      def index(self, ip):
          return self._addresses.index(ip)

      def count(self, ip):
          count = 0
          for i in self._addresses:
              if ip == i:
                  count += 1
          return count

