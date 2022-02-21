# -*- coding: utf-8 -*-

"""
Задание 24.2c

Проверить, что метод send_command класса MyNetmiko из задания 24.2b, принимает дополнительные аргументы (как в netmiko), кроме команды.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал любые аргументы, которые поддерживает netmiko.


In [2]: from task_24_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

"""

from task_24_2a import ErrorInCommand
from netmiko.cisco.cisco_ios import CiscoIosSSH
import re

class MyNetmiko(CiscoIosSSH):
        def __init__(self, **dev_params):
                super().__init__(**dev_params)
                self.enable()
                self.host = dev_params["ip"]

        def _check_error_in_command(self, command, output):
                regex = "% (?P<error>.+)"
                find_error = re.search(regex,output)
                if find_error:
                        err = find_error.group("error")
                        raise ErrorInCommand(f"При выполнении команды \"{command}\" на устройстве {self.host} возникла ошибка \"{err}\"")

        def send_command(self, command, *args, **kwargs):
                output = super().send_command(command, *args, **kwargs)
                self._check_error_in_command(command, output)
                return output

        def send_config_set(self, commands):
                commands = commands.split(',')
                self.config_mode()
                all_output = ''
                for command in commands:
                        output = super().send_config_set(command, exit_config_mode=False)
                        self._check_error_in_command(command, output)
                        all_output += output
                self.exit_config_mode()
                return all_output

