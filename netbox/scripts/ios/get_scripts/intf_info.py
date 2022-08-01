import yaml
import re
from concurrent.futures import ThreadPoolExecutor
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
from itertools import repeat
from ntc_templates.parse import parse_output

def parse_intf_info(device,commands):
    reply = {}
    with open("inventory/scrapli/ios.yml") as f:
         devices = yaml.safe_load(f)
    print(f"Идёт подключение к устройству {device}")
    try:
       with Scrapli(**devices[device]) as ssh:
            for command in commands:
                output = (ssh.send_command(command, strip_prompt=True, timeout_ops=15))
                reply[command] = output.result 
            print(f"Вывод получен для устройства {device}")
    except ScrapliException as error:
           print(error, device)
    if reply != None:
       parsed_final = {}
       for command in commands:
           filtred_list = []
           parsed_final[command] = parse_output(platform="cisco_ios", command=command, data = reply[command])
           for line in parsed_final[command]:
               result = {k : v for k, v in line.items() if v != ''}
               vlans = []
               for k,v in result.items():
                   if ("trunking_vlans" in k) & ("ALL" not in v):
                      for vlan in v:
                          vlan = vlan.split(',')
                          for vl in vlan:
                              if '-' in vl:
                                 start_vlan = vl.split('-')[0]
                                 end_vlan = vl.split('-')[1]
                                 for i in range(int(start_vlan),int(end_vlan)+1):
                                     vlans.append(str(i)) 
                              else: vlans.append(vl)
               if vlans != []:
                  result["trunking_vlans"] = vlans
               filtred_list.append(result)
           parsed_final[command] = filtred_list
       return parsed_final
    else: return None


def get_intf_info(devices, commands):
    all_devices = {}  
    virt_intfs = ['svi','loo','channel']
    with ThreadPoolExecutor(max_workers=4) as executor:
         result_command = executor.map(parse_intf_info, devices, repeat(commands))
    if result_command != None:
       for device, output in zip(devices, result_command):        
           all_devices[device] = {}
           for command in commands:
               if re.match('^show interfaces$',command):
                  for line in output[command]:
                      all_devices[device][line['interface']] = {}
                      try:
                         all_devices[device][line['interface']]['description'] = line['description']
                      except: pass
                      if 'TenGigabit' in line['interface']:
                          all_devices[device][line['interface']]['type'] = '10gbase-x-sfpp'
                      elif 'Gigabit' in line['interface']:       
                          all_devices[device][line['interface']]['type'] = '1000base-t'
                      else: all_devices[device][line['interface']]['type'] = '100base-tx'
                      for virt_intf in virt_intfs:
                          if virt_intf in line['hardware_type'].lower():
                             all_devices[device][line['interface']]['type'] = 'virtual'
                             if 'loo' in line['hardware_type'].lower():
                                all_devices[device][line['interface']]['role'] = 'loopback'
                             else: all_devices[device][line['interface']]['role'] = 'vip'
                      try:
                          all_devices[device][line['interface']]['mac'] = line['bia']
                      except: pass
                      try:
                          all_devices[device][line['interface']]['address'] = line['ip_address']
                      except: pass
                      if 'up' in line['link_status'].lower():
                         all_devices[device][line['interface']]['status'] = 'True'
                      else: all_devices[device][line['interface']]['status'] = 'False'
                      all_devices[device][line['interface']]['speed'] = line['bandwidth'].split()[0]
                      try:
                         all_devices[device][line['interface']]['duplex'] = line['duplex'].split('-')[0].lower()
                      except: pass
                      all_devices[device][line['interface']]['mtu'] = line['mtu']
               elif re.match('^show interfaces switchport$',command):
                  for line in output[command]:
                      try:
                         if 'Gi' in line['interface']:
                            intf = line['interface'].replace('Gi','GigabitEthernet')
                         elif 'Fa' in line['interface']:
                            intf = line['interface'].replace('Fa','FastEthernet')
                         elif 'Po' in line['interface']:
                            intf = line['interface'].replace('Po','Port-channel')
                         else: intf = line['interface']
                         if 'access' in line['mode'] and line['voice_vlan'] != 'none':
                            all_devices[device][intf]['mode'] = 'tagged'
                            all_devices[device][intf]['vlan'] = [line['access_vlan']]
                            all_devices[device][intf]['vlans'] = [line['voice_vlan']]
                         elif 'access' in line['mode'] and line['voice_vlan'] == 'none':
                              all_devices[device][intf]['mode'] = 'access'
                              all_devices[device][intf]['vlan'] = [line['access_vlan']]
                         elif 'trunk' in line['mode']:
                              if 'ALL' not in line['trunking_vlans']:
                                 all_devices[device][intf]['mode'] = 'tagged'
                                 all_devices[device][intf]['vlans'] = line['trunking_vlans']
                              else: all_devices[device][intf]['mode'] = 'tagged-all'
                         else: pass
                      except: pass 
       with open('results/ios/intf_info/all_devices.yaml','w') as f:
            yaml.dump(all_devices, f, default_flow_style=False)   
    else: print('Нет результата') 

if __name__ == "__main__":

   commands = ['show interfaces', 'show interfaces switchport']

   with open("inventory/scrapli/ios.yml") as f:
        devices = yaml.safe_load(f)
   get_intf_info(devices,commands)
