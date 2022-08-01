import yaml
import textfsm
import paramiko
import socket
import time
from pprint import pprint

def change_ifaces_name(device,command):
    templates_path = "templates/textfsm/routeros"
    with open("inventory/netmiko/routeros.yaml") as f:
         devices = yaml.safe_load(f)
    device = devices[device]
    print(f"Идёт подключение к устройству {device['host']}")
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect(
       hostname=device['host'],
       username= f"{device['username']}+ctw1980h4098",
       password=device['password'],
       look_for_keys=False,
       allow_agent=False
       )
    with cl.invoke_shell() as ssh:
       output = ''
       result = ''
       command_changed = command.replace(' ','_')
       path = f"{templates_path}/{command_changed}.template"
       stdin, stdout, stderr = cl.exec_command(command)
       for line in stdout:
           line = line.strip('\n')
           output += line + '\n'
       if output != None:
          with open(path) as template_file:
               template = textfsm.TextFSM(template_file)
               result = template.ParseText(output)
          result = [dict(zip(template.header, line)) for line in result]
          for line in result:
              if 'ether' in line['name']:
                  new_intf = line['name'].replace('ether','eth')
                  cl.exec_command(f"interface ethernet set {line['num']} name={new_intf}")              


if __name__ == "__main__":
   command = 'interface ethernet print'
   with open("inventory/netmiko/routeros.yaml") as f:
        devices = yaml.safe_load(f)
   for device in devices:
       try:
         change_ifaces_name(device,command)
       except: 
            print(f"Ошибка при работе на {device}")
            continue

