# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать класс CiscoTelnet, который наследует класс TelnetBase из файла base_telnet_class.py.

Переписать метод __init__ в классе CiscoTelnet таким образом:

* добавить параметры:
 * enable - пароль на режим enable
 * disable_paging - отключает постраничный вывод команд, по умолчанию равен True
* после подключения по Telnet должен выполняться переход в режим enable:
  для этого в методе __init__ должен сначала вызываться метод __init__ класса TelnetBase, а затем выполняться переход в режим enable.

Добавить в класс CiscoTelnet метод send_show_command, который отправляет команду
show и возвращает ее вывод в виде строки. Метод ожидает как аргумент одну команду.

Добавить в класс CiscoTelnet метод send_config_commands, который отправляет одну
или несколько команд на оборудование в конфигурационном режиме и возвращает ее
вывод в виде строки. Метод ожидает как аргумент одну команду (строку) или
несколько команд (список).

Пример работы класса:
In [1]: r1 = CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco')

Метод send_show_command:
In [2]: r1.send_show_command('sh clock')
Out[2]: 'sh clock\r\n*09:39:38.633 UTC Thu Oct 10 2019\r\nR1#'

Метод send_config_commands:
In [3]: r1.send_config_commands('logging 7.7.7.7')
Out[3]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 7.7.7.7\r\nR1(config)#end\r\nR1#'

In [4]: r1.send_config_commands(['interface loop77', 'ip address 107.7.7.7 255.255.255.255'])
Out[4]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop77\r\nR1(config-if)#ip address 107.7.7.7 255.255.255.255\r\nR1(config-if)#end\r\nR1#'


Тест берет значения из файла devices.yaml, поэтому если
для заданий используются другие адреса/логины, надо заменить их там.
"""

from base_telnet_class import TelnetBase

class CiscoTelnet(TelnetBase):
     def __init__(self, ip, username, password, enable, disable_paging = True):
         super().__init__(ip, username, password)
         self._telnet.write(b'enable\n')
         self._telnet.read_until(b'Password', timeout = 5)
         self._telnet.write(self._to_bytes(enable))
         self._telnet.read_until(b'#', timeout = 5)
         if disable_paging:
            self._telnet.write(b'terminal length 0\n')
            self._telnet.read_until(b'#', timeout = 5)

     def send_show_command(self, command):
         self._telnet.write(self._to_bytes(command))
         output = self._telnet.read_until(b"#", timeout = 5).decode("utf-8")
         return output

     def send_config_commands(self, commands):
         if isinstance(commands, str):
            commands = [commands]
         result = ''
         self._telnet.write(b"conf t\n")
         result += self._telnet.read_until(b"(config)#", timeout = 2).decode("utf-8")
         for command in commands:
             self._telnet.write(self._to_bytes(command))
             result += self._telnet.read_until(b"#", timeout = 2).decode("utf-8")
         self._telnet.write(b"end\n")
         result += self._telnet.read_until(b"#", timeout = 2).decode("utf-8")
         return result

     def _to_bytes(self,line):
         return f"{line}\n".encode("utf-8")
















        





























