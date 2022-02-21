# -*- coding: utf-8 -*-
'''
Задание 10.2

Скопировать класс PingNetwork из задания 9.2 и изменить его таким образом,
чтобы адреса пинговались не при вызове метода scan, а при вызове экземпляра.

Вся функциональность метода scan должна быть перенесена в метод, который отвечает
за вызов экземпляра.

Пример работы с классом PingNetwork. Сначала создаем сеть:
In [2]: net1 = IPv4Network('8.8.4.0/29')

И выделяем несколько адресов:
In [3]: net1.allocate('8.8.4.2')
   ...: net1.allocate('8.8.4.4')
   ...: net1.allocate('8.8.4.6')
   ...:

Затем создается экземпляр класса PingNetwork, сеть передается как аргумент:
In [6]: ping_net = PingNetwork(net1)

После этого экземпляр должен быть вызываемым объектом (callable):

In [7]: ping_net()
Out[7]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6'])

In [8]: ping_net(include_unassigned=True)
Out[8]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6', '8.8.4.1', '8.8.4.3', '8.8.4.5'])
'''


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
      Реализуем функционал ping при вызове экземпляра
      '''

      def __call__(self, workers = 5, include_unassigned = False): 
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
     
     
      '''
      Скрытая функция ping
      '''
      def _ping(self,ip):
          reply = subprocess.run(['ping', '-c', '3', '-n', ip], stdout=subprocess.DEVNULL)
          if reply.returncode == 0:
              return True
          else: return False

#      '''
#      Функция определяет, что пингать
#      '''
#      def _scan(self, workers, include_unassigned):
#          ping_good = []
#          ping_bad = []
#          with ThreadPoolExecutor(max_workers=workers) as executor:
#              if include_unassigned == False:
#                  result = executor.map(self._ping, self.network.allocated)
#                  for device, output in zip(self.network.allocated, result):
#                      if output:
#                          ping_good.append(device)
#                      else: ping_bad.append(device)
#              elif include_unassigned == True:
#                  result = executor.map(self._ping, self.network.host)
#                  for device, output in zip(self.network.host, result):
#                      if output:
#                          ping_good.append(device)
#                      else: ping_bad.append(device)
#          final = [ping_good, ping_bad]
#          return tuple(final)


def ping_function(network):
      net1 = IPv4Network(network)
      net1.hosts()
      net1.allocate('8.8.4.2')
      net1.allocate('8.8.4.4')
      net1.allocate('8.8.4.6')
      net1.allocated
      net1.unassigned()
      ping_net = PingNetwork(net1)
      result = ping_net()
#      result = ping_net(include_unassigned=True)
      return result

if __name__ == "__main__":
      print(ping_function('8.8.4.0/29'))    
      
          
