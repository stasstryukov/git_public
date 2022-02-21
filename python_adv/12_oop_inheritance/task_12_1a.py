# -*- coding: utf-8 -*-
"""
Задание 12.1a

Скопировать класс CiscoTelnet из задания 12.1 и добавить проверку на ошибки.

Добавить метод _check_error_in_command, который выполняет проверку на такие ошибки:
* Invalid input detected, Incomplete command, Ambiguous command

Создать исключение ErrorInCommand, которое будет генерироваться при возникновении
ошибки на оборудовании.

Метод ожидает как аргумент команду и вывод команды. Если в выводе не обнаружена ошибка,
метод ничего не возвращает. Если в выводе найдена ошибка, метод генерирует исключение
ErrorInCommand с сообщением о том какая ошибка была обнаружена, на каком устройстве и в какой команде.

Добавить проверку на ошибки в методы send_show_command и send_config_commands.

Пример работы класса с ошибками:
In [1]: r1 = CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco')

In [2]: r1.send_show_command('sh clck')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-e26d712f3ad3> in <module>
----> 1 r1.send_show_command('sh clck')
...
ErrorInCommand: При выполнении команды "sh clck" на устройстве 192.168.100.1 возникла ошибка "Invalid input detected at '^' marker.

In [3]: r1.send_config_commands('loggg 7.7.7.7')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-3-ab4a1ce52554> in <module>
----> 1 r1.send_config_commands('loggg 7.7.7.7')
...
ErrorInCommand: При выполнении команды "loggg 7.7.7.7" на устройстве 192.168.100.1 возникла ошибка "Invalid input detected at '^' marker.

Без ошибок:
In [4]: r1.send_show_command('sh clock')
Out[4]: 'sh clock\r\n*09:39:38.633 UTC Thu Oct 10 2019\r\nR1#'

In [5]: r1.send_config_commands('logging 7.7.7.7')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 7.7.7.7\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop77', 'ip address 107.7.7.7 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop77\r\nR1(config-if)#ip address 107.7.7.7 255.255.255.255\r\nR1(config-if)#end\r\nR1#'



Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.
R1(config)#logging
% Incomplete command.

R1(config)#sh i
% Ambiguous command:  "sh i"
"""

# списки команд с ошибками и без:
config_commands_errors = ["logging 0255.255.1", "logging", "sh i"]
correct_config_commands = ["logging buffered 20010", "ip http server"]


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
         check = self._check_error_in_command(command, output)
         if check != None:
            output = check
         return output

     def send_config_commands(self, commands):
         if isinstance(commands, str):
            commands = [commands]
         output = ''
         self._telnet.write(b"conf t\n")
         output += self._telnet.read_until(b"(config)#", timeout = 2).decode("utf-8")
         for command in commands:
             self._telnet.write(self._to_bytes(command))
             output += self._telnet.read_until(b"#", timeout = 2).decode("utf-8")
         self._telnet.write(b"end\n")
         output += self._telnet.read_until(b"#", timeout = 2).decode("utf-8")
         check = self._check_error_in_command(command, output)
         if check != None:
            output = check
         return output

     def _to_bytes(self,line):
         return f"{line}\n".encode("utf-8")

     def _check_error_in_command(self, command, output):
         print(output)
         if 'Invalid input detected' in output:
            raise ErrorInCommand(f"При выполнении команды {command} на устройстве {self.ip} возникла ошибка \"Invalid input detected at '^' marker\" ")
         elif 'Incomplete command' in output:
            raise ErrorInCommand(f"При выполнении команды {command} на устройстве {self.ip} возникла ошибка \"Incomplete command\" ")
         elif 'Ambiguous command' in output:
            raise ErrorIncommand(f"При выполнении команды {command} на устройстве {self.ip} возникла ошибка \"Ambiguous command\" ")
         else: result = None
         return result

class ErrorInCommand(Exception):
      pass

def check_task(ip,username,password,enable):
    r1 = CiscoTelnet(ip,username,password,enable)
    r1.send_show_command('sh clck')
    print("*" * 30)
    r1.send_config_commands('loggg 7.7.7.7')
    print("*" * 30)
    r1.send_show_command('sh clock')
    print("*" * 30)
    r1.send_config_commands('logging 7.7.7.7')
    print("*" * 30)
    r1.send_config_commands(['interface loop77', 'ip address 107.7.7.7 255.255.255.255'])    

if __name__ == "__main__":
    result = check_task('192.168.1.100', 'cisco', 'cisco', 'cisco')
