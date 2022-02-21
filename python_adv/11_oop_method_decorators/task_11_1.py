# -*- coding: utf-8 -*-
"""
Задание 11.1
Скопировать класс IPv4Network из задания 9.1.
Переделать класс таким образом, чтобы методы hosts и unassigned
стали переменными, но при этом значение переменной экземпляра вычислялось
каждый раз при обращении и запись переменной была запрещена.
Пример создания экземпляра класса:
In [1]: net1 = IPv4Network('8.8.4.0/29')
In [2]: net1.hosts
Out[2]: ('8.8.4.1', '8.8.4.2', '8.8.4.3', '8.8.4.4', '8.8.4.5', '8.8.4.6')
In [3]: net1.allocate('8.8.4.2')
In [4]: net1.allocate('8.8.4.3')
In [5]: net1.unassigned
Out[5]: ('8.8.4.1', '8.8.4.4', '8.8.4.5', '8.8.4.6')
Запись переменной:
In [6]: net1.unassigned = 'test'
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-6-c98e898835e1> in <module>
----> 1 net1.unassigned = 'test'
AttributeError: can't set attribute
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
     
