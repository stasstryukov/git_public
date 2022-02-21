# -*- coding: utf-8 -*-
"""
Задание 9.2

Создать класс PingNetwork. При создании экземпляра класса PingNetwork, как аргумент передается экземпляр класса IPv4Network.

У класса PingNetwork должны быть методы _ping и scan

Метод _ping с параметром ip: должен пинговать один IP-адрес и возвращать
* True - если адрес пингуется
* False - если адрес не пингуется

Метод scan с таким параметрами:

* workers - значение по умолчанию 5
* include_unassigned - значение по умолчанию False

Метод scan:

* Пингует адреса из сети, которая передается как аргумент при создании экземпляра.
* Адреса должны пинговаться в разных потоках, для этого использовать concurrent.futures.
* По умолчанию, пингуются только адреса, которые находятся в атрибуте allocated.
  Если параметр include_unassigned равен True, должны пинговаться и адреса unassigned.
* Метод должен возвращать кортеж с двумя списками: список доступных IP-адресов и список недоступных IP-адресов



Пример работы с классом PingNetwork. Сначала создаем сеть:
In [3]: net1 = IPv4Network('8.8.4.0/29')

И выделяем несколько адресов:
In [4]: net1.allocate('8.8.4.2')
   ...: net1.allocate('8.8.4.4')
   ...: net1.allocate('8.8.4.6')
   ...:

In [5]: net1.allocated
Out[5]: ('8.8.4.2', '8.8.4.4', '8.8.4.6')

In [6]: net1.unassigned()
Out[6]: ('8.8.4.1', '8.8.4.3', '8.8.4.5')

Затем создается экземпляр класса PingNetwork, а сеть передается как аргумент:

In [8]: ping_net = PingNetwork(net1)

Пример работы метода scan:
In [9]: ping_net.scan()
Out[9]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6'])

In [10]: ping_net.scan(include_unassigned=True)
Out[10]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6', '8.8.4.1', '8.8.4.3', '8.8.4.5'])

"""
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import subprocess


class IPv4Network:
      '''
      Класс IPv4Network
      '''
      def __init__(self, network):
          self.net1 = ipaddress.ip_network(network)
          self.address = network.split('/')[0]
          mask = network.split('/')[1]
          self.mask = int(mask)
          self.broadcast = self.net1.broadcast_address
          self.allocated = ()

      '''
      Список хостов
      '''
      def hosts(self):
          ip_list = []
          ips = self.net1.hosts()
          for ip in ips:
              ip_list.append(str(ip))
          self.host = tuple(ip_list)
          return self.host

      '''
      Присваиваем адреса
      '''
      def allocate(self, ip_addr):
          allocated = list(self.allocated)
          if ip_addr in self.host:
                 allocated.append(ip_addr)
          self.allocated = tuple(allocated) 

      '''
      Список не присвоенных адресов
      '''
      def unassigned(self):
          unassign = []
          print(self.allocated)
          for ip in self.net1.hosts():
              if str(ip) not in self.allocated:
                  unassign.append(str(ip))
          return(tuple(unassign))

class PingNetwork:
      '''
      Класс PingNetwork
      '''
      def __init__(self, network):
          self.network = network
      
      '''
      Скрытая функция ping
      '''
      def _ping(self,ip):
          reply = subprocess.run(['ping', '-c', '3', '-n', ip], stdout=subprocess.DEVNULL)
          if reply.returncode == 0:
              return True
          else: return False

      '''
      Функция определяет, что пингать
      '''
      def scan(self, workers = 5, include_unassigned = False):
          ping_good = []
          ping_bad = []
          with ThreadPoolExecutor(max_workers=workers) as executor:
              if include_unassigned == False:
                  result = executor.map(self._ping, self.network.allocated)
                  for device, output in zip(self.network.allocated, result):
                      if output:
                          ping_good.append(device)
                      else: ping_bad.append(device)
              elif include_unassigned == True:
                  result = executor.map(self._ping, self.network.host)
                  for device, output in zip(self.network.host, result):
                      if output:
                          ping_good.append(device)
                      else: ping_bad.append(device)
          final = [ping_good, ping_bad]
          return tuple(final)


def ping_function(network):
      net1 = IPv4Network(network)
      net1.hosts()
      net1.allocate('8.8.4.2')
      net1.allocate('8.8.4.4')
      net1.allocate('8.8.4.6')
      net1.allocated
      net1.unassigned()
      ping_net = PingNetwork(net1)
#      result = ping_net.scan()
      result = ping_net.scan(include_unassigned=True)
      return result

if __name__ == "__main__":
      print(ping_function('8.8.4.0/29'))    
      
          
