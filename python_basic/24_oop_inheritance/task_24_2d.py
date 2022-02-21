# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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

        def send_command(self, command, *args, **kwargs):
                output = super().send_command(command, *args, **kwargs)
                self._check_error_in_command(command, output)
                return output

        def send_config_set(self, commands, ignore_errors = True):
                commands = commands.split(',')
                if ignore_errors:
                     output = super().send_config_set(commands)
                     return output
                all_output = ''
                for command in commands:
                        output = super().send_config_set(command, exit_config_mode=False)
                        if ignore_errors == False:
                             self._check_error_in_command(command, output)
                        all_output += output
                self.exit_config_mode()
                return all_output


