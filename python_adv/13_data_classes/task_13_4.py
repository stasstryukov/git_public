# -*- coding: utf-8 -*-
"""
Задание 13.4

Создать класс IPv4Network с использованием dataclass. У экземпляров класса должны быть
доступны:
* переменные: network, broadcast, hosts, allocated, unassigned
* метод allocate

Пример создания экземпляра класса:

In [3]: net1 = IPv4Network('10.1.1.0/29')

После этого, должна быть доступна переменная network:
In [6]: net1.network
Out[6]: '10.1.1.0/29'


Broadcast адрес должен быть записан в атрибуте broadcast:

In [7]: net1.broadcast
Out[7]: '10.1.1.7'

Также должен быть создан атрибут allocated в котором будет
храниться список с адресами, которые назначены на каком-то
устройстве/хосте. Изначально атрибут равен пустому списку:

In [8]: print(net1.allocated)
[]


Атрибут hosts должен возвращать список IP-адресов, которые входят в сеть,
не включая адрес сети и broadcast:

In [9]: net1.hosts
Out[9]: ['10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5', '10.1.1.6']

Метод allocate ожидает как аргумент IP-адрес. Указанный адрес
должен быть записан в список в атрибуте net1.allocated и удален из списка unassigned:

In [10]: net1 = IPv4Network('10.1.1.0/29')

In [11]: print(net1.allocated)
[]

In [12]: net1.allocate('10.1.1.6')

In [13]: net1.allocate('10.1.1.3')

In [14]: print(net1.allocated)
['10.1.1.6', '10.1.1.3']


Атрибут unassigned возвращает возвращает список со свободными адресами:

In [15]: net1 = IPv4Network('10.1.1.0/29')

In [16]: net1.allocate('10.1.1.4')
    ...: net1.allocate('10.1.1.6')
    ...: net1.allocate('10.1.1.8')
    ...:

In [17]: net1.unassigned
Out[17]: ['10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.5']

"""


import ipaddress
from dataclasses import dataclass, field

@dataclass           
class IPv4Network:
      _net1: str
      _network: str = field(init=False, repr=False)
      _broadcast: str = field(init=False, repr=False)
      _hosts: list = field(default_factory=list)
      _allocated: list = field(default_factory=list)
      _unassigned: list = field(default_factory=list)

      def __post_init__(self):
          self._network = ipaddress.ip_network(self._net1)
          self._allocated = list(self._allocated)

      @property
      def network(self):
          return str(self._network)

      @property
      def broadcast(self):
          return str(self._network.broadcast_address)

      @property
      def hosts(self):
          ip_list = []
          ips = self._network.hosts()
          for ip in ips:
              ip_list.append(str(ip))
          self.host = list(ip_list)
          return self.host

      @property
      def allocated(self):
          return self._allocated

      def allocate(self, ip_addr):
          if ip_addr in self.hosts:
                 self.allocated.append(ip_addr)

      @property
      def unassigned(self):
          unassign = []
          for ip in self._network.hosts():
              if str(ip) not in self.allocated:
                  unassign.append(str(ip))
          return unassign


