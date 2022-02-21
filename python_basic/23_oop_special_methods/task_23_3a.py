# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

class Topology:
        def __init__(self, topology_dict):
                self.topology = self._normalize(topology_dict)

        def _normalize(self,topology_dict):
                self.dict = {}
                for key, value in topology_dict.items():
                        if self.dict.get(value) != key:
                                self.dict[key] = value
                return self.dict

        def delete_link(self,local,remote):
                if self.topology.get(local) == remote:
                        del self.topology[local]
                if self.topology.get(remote) == local:
                        del self.topology[remote]
                else: print('Нет такой записи')

        def delete_device(self,device):
                orig = 0
                new = 0
                self.tmp_dict = self.topology.copy()
                for local, remote in tmp_dict.items():
                        if (local[0] == device) or (remote[0] == device):
                                del self.topology[local]
                for value in tmp_dict:
                        orig = orig + 1
                for value in self.topology:
                        new = new + 1
                if orig == new:
                        print('Устройства нет')

#       def add_link(self,local,remote):
#                if (self.topology.get(local) == remote) or (self.topology.get(remote) == local):
#                        print('Соедение уже существует')
#               elif ((local or remote) in self.topology.keys()) or ((local or remote) in self.topology.values()):
#                       print('Cоединение с одним из портов существует')
#               else: self.topology[local] = remote

        def __add__(self, var2):
                new_topo = self.topology.copy()
                new_topo.update(var2.topology)

        def __iter__(self):
                return iter(self.topology.items())
