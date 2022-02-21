# -*- coding: utf-8 -*-
'''
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12': 10,
                       'FastEthernet0/14': 11,
                       'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def get_int_vlan_map(config_filename='config_sw2.txt'):
        dict_access = {}
        dict_trunk = {}
        line_test = ''
        with open(config_filename) as config:
                for line in config:
                        if 'FastEthernet' in line:
                                intf = line.split()[1]
                        elif 'access vlan' in line:
                                vlans = line.split()[-1]
                                dict_access[intf] = int(vlans)
                                line_test = line_test + line
                        elif 'allowed vlan' in line:
                                line_test = line_test + line
                        elif ('duplex auto' in line and ('access vlan' in line_test or 'allowed vlan' in line_test)):
                                line_test = ''
                        elif ('duplex auto' in line and ('access vlan' not in line_test or 'allowed vlan' not in line_test)):
                               dict_access[intf] = 1

        with open(config_filename) as config:
                for line in config:
                        if 'FastEthernet' in line:
                                intf = line.split()[1]
                        elif 'allowed vlan' in line:
                                line_test = line_test + line
                                vlans = line.split()
                                vlans = vlans[-1].split(',')
                                vlans_list = []
                                for vlan in vlans:
                                        vlans_list.append(int(vlan))
                                dict_trunk[intf] = vlans_list

        return dict_access, dict_trunk



print(get_int_vlan_map())

