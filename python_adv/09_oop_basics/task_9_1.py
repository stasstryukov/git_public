# -*- coding: utf-8 -*-
"""
Задание 9.1

Создать класс IPv4Network, который представляет сеть.
При создании экземпляра класса, как аргумент передается строка с адресом сети.

Для реализации функционала класса можно использовать модуль ipaddress.

Пример создания экземпляра класса:

In [3]: net1 = IPv4Network('10.1.1.0/29')

После этого, должны быть доступны переменные address и mask:
In [5]: net1.address
Out[5]: '10.1.1.0'

In [6]: net1.mask
Out[6]: 29


Broadcast адрес должен быть записан в атрибуте broadcast:

In [7]: net1.broadcast
Out[7]: '10.1.1.7'

Также должен быть создан атрибут allocated в котором будет
храниться кортеж с адресами, которые назначены на каком-то
устройстве/хосте. Изначально атрибут равен пустому кортежу:

In [8]: print(net1.allocated)
()


Метод hosts должен возвращать кортеж IP-адресов, которые входят в сеть,
не включая адрес сети и broadcast:

In [9]: net1.hosts()
Out[9]: ('10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5', '10.1.1.6')

Метод allocate ожидает как аргумент IP-адрес. Указанный адрес
должен быть записан в кортеж в атрибуте net1.allocated:

In [10]: net1 = IPv4Network('10.1.1.0/29')

In [11]: print(net1.allocated)
()

In [12]: net1.allocate('10.1.1.6')

In [13]: net1.allocate('10.1.1.3')

In [14]: print(net1.allocated)
('10.1.1.6', '10.1.1.3')


Метод unassigned возвращает возвращает кортеж со свободными адресами:

In [15]: net1 = IPv4Network('10.1.1.0/29')

In [16]: net1.allocate('10.1.1.4')
    ...: net1.allocate('10.1.1.6')
    ...:

In [17]: net1.unassigned()
Out[17]: ('10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.5')

"""
import ipaddress

class IPv4Network:
      def __init__(self, network):
          self.net1 = ipaddress.ip_network(network)
          self.address = network.split('/')[0]
          mask = network.split('/')[1]
          self.mask = int(mask)
          self.addresses = [str(ip) for ip in self.net1.hosts()]
          self.broadcast = self.net1.broadcast_address
          self.allocated = ()

      def hosts(self):
          return tuple(self.addresses)

      def allocate(self, ip_addr):
          allocated = list(self.allocated)
          if ip_addr in self.addresses:
                 allocated.append(ip_addr)
          self.allocated = tuple(allocated)

      def unassigned(self):
          unassign = []
          for ip in self.net1.hosts():
              if str(ip) not in self.allocated:
                  unassign.append(str(ip))
          return(tuple(unassign))


def ip(ip):
    ip1 = IPv4Network(ip)
    print("Net:",ip1.address)
    print("Mask",ip1.mask)
    print("Bcast",ip1.broadcast)
    print("Empty",ip1.allocated)
    ip1.allocate("100.7.1.8")
    ip1.allocate("100.7.1.3")
    ip1.allocate("100.7.1.2")
    print("Allocated",ip1.allocated)
    print("Unassigned",ip1.unassigned())

if __name__ == "__main__":
      result = ip("100.7.1.0/28")
     
