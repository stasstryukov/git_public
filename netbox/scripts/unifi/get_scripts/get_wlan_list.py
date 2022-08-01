import yaml
from pprint import pprint
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor
from unificontrol import UnifiClient

def parse_wlans_info(device, commands):
    reply = {}
    with open("inventory/api/wireless_controllers.yaml") as f:
        devices = yaml.safe_load(f)
    device = devices[device]
    cl = UnifiClient(host=f"{device['ip']}",username=f"{device['username']}",password=f"{device['password']}",site=f"{device['site']}")
    for command in commands:
        result = eval(f"cl.{command}")
        reply[command] = result
    return reply

def get_wlans_info(devices, commands):
    all_devices = {}
    filtred_list = []
    with ThreadPoolExecutor(max_workers=5) as executor:
         result_command = executor.map(parse_wlans_info,devices,repeat(commands))
    if result_command != None:
         for device, output in zip(devices, result_command):
             all_devices[device] = []
             for command in commands:
                 if 'list_wlanconf' in command:
                    results = []
                    for line in output[command]:
                        result = {}
                        if 'krd' in device:
                           result['description'] = 'KRD'
                        else: result['description'] = 'DIN'
                        result['ssid'] = line['name']
                        if 'wpapsk' in line['security']:
                            result['auth_type'] = 'wpa-personal'
                        elif 'wpaeap' in line['security']:
                            result['auth_type'] = 'wpa-enterprise'
                        else: result['auth_type'] = line['security']
                        result['vlan_id'] = line['networkconf_id']
                        if 'personal' in result['auth_type']:
                           result['auth_psk'] = line['x_passphrase']
                        results.append(result)
                        try:
                           result['auth_cipher'] = line['pmf_cipher']
                        except: pass
                 elif 'list_networkconf' in command:
                       for line in output[command]:
                           for line2 in results:
                               try:
                                  if line['_id'] == line2['vlan_id']:
                                     line2['vlan'] = str(line['vlan'])
                               except: pass
             for line in results:
                 try: 
                     del line['vlan_id']
                 except: pass
             all_devices[device] = results
         try:
           tmp_list = []
           for v in all_devices.values():
               for line in v:
                   tmp_list.append(line)
           [filtred_list.append(line) for line in tmp_list if line not in filtred_list]
         except: pass
         with open('results/unifi/wifi_info/all_wlans.yaml','w') as f:
              yaml.dump(all_devices, f, default_flow_style=False)
    else: print('Нет результата')
 
        
if __name__ == "__main__":
   commands = ['list_wlanconf()','list_networkconf()']
   with open("inventory/api/wireless_controllers.yaml") as f:
        devices = yaml.safe_load(f)
   get_wlans_info(devices, commands)
