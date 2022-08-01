import yaml
import textfsm
import re
import paramiko
import socket
import time
from pprint import pprint
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor
#from functools import wraps

#def current_func(func):
#    @wraps(func)
#    def wrapper(*args, **kwargs):
#        print(f"Работает функция {func.__name__}")
#        return func(*args,**kwargs)
#    return wrapper

#@current_func
def parse_device_info(device,command):
    template_path = "templates/textfsm/routeros"
    command_changed = command.replace(' ','_')
    parsed_final = {}
    output = ''
    with open("inventory/netmiko/routeros.yaml") as f:
         devices = yaml.safe_load(f)
    print(f"Идёт подключение к устройству {device}")
    device = devices[device]
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect(
       hostname=device['host'],
       username= f"{device['username']}+ctw1024h4098",
       password=device['password'],
       look_for_keys=False,
       allow_agent=False
       )
    with cl.invoke_shell() as ssh:
       stdin, stdout, stderr = cl.exec_command(command)
       for line in stdout:
           output += line.strip() + '\n'
    print("Вывод получен") 
    path = f"{template_path}/{command_changed}.template"
    with open(path) as template_file:
         template = textfsm.TextFSM(template_file)
         result = template.ParseText(output)
         result = [dict(zip(template.header,line)) for line in result]
    for line in result:
        parsed_final = {key:value for key,value in line.items() if value != ''}    
    return parsed_final 

#@current_func
def get_device_info(devices,command):
    dev_locs = {
                        "KRD" : "Krasnodar",
                        "DIN" : "Dinskaya",
                        "KLB" : "Kalininskaya",
                        "KOR" : "Korenovsk",
                        "KUR" : "Petropavlovskaya",
                        "TLB" : "Starotitarovskaya"
                    }

    dev_roles = {
                    "GW" : "Border router",
                    "AL" : "Access switch",
                    "DL" : "Collapsed core switch"    
                  }  

    all_devices = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
         result_command = executor.map(parse_device_info, devices, repeat(command))
    if result_command != None:
       device_list = []
       for device, output in zip(devices, result_command):
           device_dict = {}
           regex_dev_name = r'(?P<dev_loc>.+?)-(?P<dev_type>.+)-.+'
           regex_dev_role = r'.+-(?P<role>\w+)' 
           match_dev_name = re.search(regex_dev_name, device)
           dev_loc = match_dev_name.group(1)
           dev_type = match_dev_name.group(2)
           match_dev_role = re.search(regex_dev_role, dev_type)
           if match_dev_role:
              dev_role = match_dev_role.group(1)
           device_dict['name'] = device
           if 'GW' in dev_type:
               device_dict['device_role'] = dev_roles['GW']
           else: device_dict['device_role'] = dev_roles[dev_role]
           device_dict['manufacturer'] = 'Mikrotik'
           device_dict['device_type'] = output['hardware_model']
           device_dict['serial_number'] = output['serial_number']
           device_dict['region'] = 'Краснодарский край'
           device_dict['site'] = dev_locs[dev_loc]
           device_dict['status'] = 'Active'
           device_dict['platform'] = 'RouterOS'
           device_dict['changed'] = 'yes'
           device_list.append(device_dict)
       all_devices['devices'] = device_list
       pprint(all_devices)
       with open('results/mikrotik/device_list/all_devices.yaml','w') as f:
            yaml.dump(all_devices, f, default_flow_style=False, encoding="utf8",allow_unicode=True) 
    else: print("Нет результата")

if __name__ == "__main__":
    command = "/system routerboard print without-paging"
    with open("inventory/netmiko/routeros.yaml") as f:
         devices = yaml.safe_load(f)
    get_device_info(devices,command)
