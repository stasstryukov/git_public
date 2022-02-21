# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

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

        def send_command(self, command):
                output = super().send_command(command)
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
