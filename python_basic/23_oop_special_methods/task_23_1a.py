# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""


class IPAddress:
        def __init__(self, ipaddress):
                self.ip, self.mask = ipaddress.split("/")
                self._checkip(self.ip)
                self._checkmask(self.mask)
                if (self._checkip(self.ip) is True) and (self._checkmask(self.mask) is True):
                        print(ipaddress)

        def __str__(self):
                return f"IPAddress: {self.ip}/{self.mask}"

        def __repr__(self):
                return f"IPAddress('{self.ip}/{self.mask}')"


        def _checkip(self, ip):
                octets = ip.split(".")
                octet_count = 0
                if len(octets) == 4:
                        for octet in octets:
                                octet = int(octet)
                                if (octet_count != 3) and ((octet > 1) and (octet < 255)):
                                        octet_count =+ 1
                                        pass
                                elif (octet_count != 3) and ((octet < 1) or (octet > 255)):
                                        raise ValueError("IP плохой")
                                        break
                                elif (octet_count == 3) and ((octet > 1) and (octet < 254)):
                                        return True
                                elif (octet_count == 3) and ((octet < 1) or (octet > 254)):
                                        raise ValueError("IP плохой")
                else: raise ValueError("IP плохой")

        def _checkmask(self,mask):
                if ((int(mask) > 8) and (int(mask) < 32)):
                        return True
                else: raise ValueError('Маска плохая')
