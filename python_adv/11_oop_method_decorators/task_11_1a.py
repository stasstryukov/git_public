# -*- coding: utf-8 -*-
"""
Задание 11.1a

Скопировать класс IPv4Network из задания 11.1.
Добавить метод from_tuple, который позволяет создать экземпляр класса IPv4Network
из кортежа вида ('10.1.1.0', 29).

Пример создания экземпляра класса:

In [3]: net2 = IPv4Network.from_tuple(('10.1.1.0', 29))

In [4]: net2
Out[4]: IPv4Network(10.1.1.0/29)

"""

import ipaddress

class IPv4Network:
      def __init__(self, network):
          self.net1 = ipaddress.ip_network(network)
          self.address = network.split('/')[0]
          mask = network.split('/')[1]
          self.mask = int(mask)
          self.broadcast = str(self.net1.broadcast_address)
          self.allocated = ()
          self._hosts = None
          self._unassigned = None
      
      @classmethod
      def from_tuple(cls, tuple_network):
          ip, mask = tuple_network
          return cls(f"{ip}/{mask}")          

      @property
      def hosts(self):
          ip_list = []
          ips = self.net1.hosts()
          for ip in ips:
              ip_list.append(str(ip))
          self.host = tuple(ip_list)
          return self.host

      def allocate(self, ip_addr):       
          allocated = list(self.allocated)
          if ip_addr in self.hosts:
                 allocated.append(ip_addr)
          self.allocated = tuple(allocated)

      @property
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
    print("Hosts",ip1.hosts)
    ip1.allocate("100.7.1.3")
    ip1.allocate("100.7.1.4")
    print("Allocated",ip1.allocated)
    print("Unassigned",ip1.unassigned)

if __name__ == "__main__":
      result = ip("100.7.1.0/29")
  
