# -*- coding: utf-8 -*-

"""
Задание 23.1

В этом задании необходимо создать класс IPAddress.

При создании экземпляра класса, как аргумент передается IP-адрес и маска,
а также должна выполняться проверка корректности адреса и маски:
* Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой
   - каждое число в диапазоне от 0 до 255
* маска считается корректной, если это число в диапазоне от 8 до 32 включительно

Если маска или адрес не прошли проверку, необходимо сгенерировать исключение ValueError с соответствующим текстом (вывод ниже).

Также, при создании класса, должны быть созданы два атрибута экземпляра: ip и mask, в которых содержатся адрес и маска, соответственно.

Пример создания экземпляра класса:
In [1]: ip = IPAddress('10.1.1.1/24')

Атрибуты ip и mask
In [2]: ip1 = IPAddress('10.1.1.1/24')

In [3]: ip1.ip
Out[3]: '10.1.1.1'

In [4]: ip1.mask
Out[4]: 24

Проверка корректности адреса (traceback сокращен)
In [5]: ip1 = IPAddress('10.1.1/24')
---------------------------------------------------------------------------
...
ValueError: Incorrect IPv4 address

Проверка корректности маски (traceback сокращен)
In [6]: ip1 = IPAddress('10.1.1.1/240')
---------------------------------------------------------------------------
...
ValueError: Incorrect mask

"""

class IPAddress:
	def __init__(self, ipaddress):
		self.ip, self.mask = ipaddress.split("/")
		self._checkip(self.ip)
		self._checkmask(self.mask)
		if (self._checkip(self.ip) is True) and (self._checkmask(self.mask) is True):
			print(ipaddress)


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
