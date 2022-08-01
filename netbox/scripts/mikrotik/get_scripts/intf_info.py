import yaml
import textfsm
import paramiko
import socket
import time
import re
from pprint import pprint
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

def parse_intf_info(device,commands):
    templates_path = "templates/textfsm/routeros"
    reply = {}
    filtred_dict = []
    intf_list = []
    result = ''
    with open("inventory/netmiko/routeros.yaml") as f:
        devices = yaml.safe_load(f)
    device_name = device
    device = devices[device]
    print(f"Идёт подключение к устройству {device_name}")
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
         stdin, stdout, stderr = cl.exec_command('interface print detail')
         for line in stdout:
             line = line.strip()
             match = re.search(r'^.*?name=\"(?P<iface>[eth|spf]\S+)\"', line)
             if match:
                intf_list.append(match.group(1)) 
         for command in commands:
             if 'interface ethernet monitor' in command:
                  reply[command] = {}
                  output = ''
                  for intf in intf_list:
                      stdin, stdout, stderr = cl.exec_command(f"{command} {intf} once")
                      for line in stdout:
                          line = line.strip()
                          if 'Flags' in line:
                             pass
                          output += line + '\n'
                      reply[command][intf] = output
             elif 'interface ethernet monitor' not in command:
                  output = ''
                  stdin, stdout, stderr = cl.exec_command(command)
                  for line in stdout:
                      line = line.strip()
                      if 'Flags' in line:
                         pass
                      match = re.search(r'^\s*\d+\s+', line)
                      if match:
                         output += '\n'+line
                      else: output += ' '+line  
                  reply[command] = output
         print(f"Вывод получен для устройства {device_name}")
         if reply != None:
            parsed_final = {}
            for command in commands:
                parsed_final[command] = []
                command_changed = command.replace(' ','_')
                path = f"{templates_path}/{command_changed}.template"
                if 'interface ethernet monitor' in command:
                   with open(path) as template_file:
                        template = textfsm.TextFSM(template_file)
                        for intf in intf_list:
                            result = template.ParseText(reply[command][intf])
                            result = [dict(zip(template.header, line)) for line in result]            
                        parsed_final[command] = result 
                if 'interface ethernet monitor' not in command:
                   with open(path) as template_file:
                        template = textfsm.TextFSM(template_file)
                        result = template.ParseText(reply[command])
                   result = [dict(zip(template.header, line)) for line in result]
                   for line in result:
                       filtred_dict = {key:value for key,value in line.items() if value != ''}                    
                       for key,value in line.items():
                           for e in value:
                               if ',' in e:
                                   value = e.split(',')
                                   filtred_dict[key]=value
                               elif '""' in e:
                                   del filtred_dict[key]
                               else: filtred_dict[key]=value
                       parsed_final[command].append(filtred_dict)
            return parsed_final
         else: return None


def get_intf_info(devices, commands):
    all_devices = {}
    virt_intfs = ['vlan','l2tp','ppp','loo','bridge','wlan','cap']
    with ThreadPoolExecutor(max_workers=10) as executor:
         result_command = executor.map(parse_intf_info, devices, repeat(commands))
    if result_command != None:
       for device, output in zip(devices, result_command):
           all_devices[device] = {}
           for command in commands:
               if re.match('^interface print detail$',command):
                  for line in output[command]:
                      intf_name = line['name']
                      if ('-' in intf_name) & ('eth' in intf_name):
                         intf_name = intf_name.split('-')[0]
                      all_devices[device][intf_name] = {}
                      all_devices[device][intf_name]['description'] = line['name']
                      for virt_intf in virt_intfs:
                         if virt_intf in line['name'].lower():
                            all_devices[device][intf_name]['type'] = 'virtual'
                            if 'loo' in line['name'].lower():
                                all_devices[device][intf_name]['role'] = 'loopback'
                            else: all_devices[device][intf_name]['role'] = 'vip'
                      try:
                         all_devices[device][intf_name]['mac'] = line['mac']
                      except: pass
                      if 'isUp' in line.keys():
                         if 'R' in line['isUp']:  
                             all_devices[device][intf_name]['isUp'] = 'True'
                         else: all_devices[device][intf_name]['isUp'] = 'False'
                      else: all_devices[device][intf_name]['isUp'] = 'False'
                      try: 
                         all_devices[device][intf_name]['mtu'] = line['mtu']
                      except: pass
               elif re.match('^interface ethernet monitor$',command):
                  for line in output[command]:
                      intf_name = line['name']
                      if ('-' in intf_name) & ('eth' in intf_name):
                         intf_name = intf_name.split('-')[0]
                      if 'yes' in line['duplex']:                             
                          all_devices[device][intf_name]['duplex']='full'
                      else: all_devices[device][intf_name]['duplex']='half'
                      if 'Gbps' in line['speed']:
                          all_devices[device][intf_name]['speed']='1000000'
                          all_devices[device][intf_name]['type'] = '1000base-t'
                      elif ('Mbps' in line['speed']) & ('100' in line['speed']):
                          all_devices[device][intf_name]['speed']='100000'
                          all_devices[device][intf_name]['type'] = '100base-tx'
               elif re.match('interface bridge vlan print detail', command):
                    for line in output[command]:
                        if 'tagged' in line.keys():
                          for intf in line['tagged']:
                              if ('-' in intf) & ('eth' in intf):
                                 intf = intf.replace(' ','').split('-')[0]
                                 all_devices[device][intf]['mode'] = 'tagged'
                              if 'vlans' not in all_devices[device][intf].keys():
                                  all_devices[device][intf]['vlans'] = []
                              all_devices[device][intf]['vlans'].append(line['vlan_id'])
                        if 'untagged' in line.keys():
                          for intf in line['untagged']:
                              if ('-' in intf) & ('eth' in intf):
                                 intf = intf.replace(' ','').split('-')[0]
                              else: intf = intf.replace(' ','')
                              all_devices[device][intf]['mode'] = 'access'
                              all_devices[device][intf]['vlan'] = line['vlan_id']
               elif re.match('ip address print',command):
                    for line in output[command]:
                      intf_name = line['name']
                      if ('-' in intf_name) & ('eth' in intf_name):
                         intf_name = intf_name.split('-')[0]    
                      all_devices[device][intf_name]['address'] = line['ip_address']               
               else: pass
       with open('results/mikrotik/intf_info/all_devices.yaml','w') as f:
            yaml.dump(all_devices, f, default_flow_style=False)
    else: print('Нет результата')



if __name__ == "__main__":
   commands = ['interface print detail','interface ethernet monitor','interface bridge vlan print detail','ip address print']
   with open("inventory/netmiko/routeros.yaml") as f:
        devices = yaml.safe_load(f)
   get_intf_info(devices,commands)
