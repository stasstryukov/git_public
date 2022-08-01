import yaml
import pynetbox
import requests
from pprint import pprint

def intf_add(device_list, intf_dict, inft_info):
    nb = pynetbox.api("https://netbox/", token="token")
    session = requests.Session()
    session.verify = False
    nb.http_session = session
    for device in device_list:
        netbox_device = nb.dcim.devices.get(name = device)
        for intf in intf_dict[device]:
               params = {}
               try:
                   params['device'] = netbox_device.id
               except: pass
               try:  
                   params['name'] = intf
               except: pass
               try:
                   params['type'] = intf_info[device][intf]['type']
               except: pass
               try:
                   params['enabled'] = intf_info[device][intf]['isUp']
               except: pass
               try:
                   params['mtu'] = intf_info[device][intf]['mtu']
               except: pass
               try:        
                   params['mac_address'] = intf_info[device][intf]['mac']
               except: pass
               try:
                   params['speed'] = inft_info[device][intf]['speed']
               except: pass
               try:
                   params['duplex'] = intf_info[device][intf]['duplex']
               except: pass
               try: 
                   params['description'] = inft_info[device][intf]['description']
               except: pass
               try:
                   params['mode'] = intf_info[device][intf]['mode']
               except: pass
               try:
                   vlan = intf_info[device][intf]['vlan']
                   vlan_id = nb.ipam.vlans.get(vid=vlan)
                   params['untagged_vlan'] = vlan_id.id
               except: pass
               try:
                   vlans = intf_info[device][intf]['vlans']
                   if 'ALL' not in vlans:
                       vlans_ids = []
                       for vlan in vlans:
                           vlan_id = nb.ipam.vlans.get(vid=vlan)
                           vlans_ids.append(vlan_id.id)
                       params['tagged_vlans'] = vlans_ids
                   else: pass
               except: pass
               try:
                   nb.dcim.interfaces.create(params)
               except pynetbox.core.query.RequestError as e:
                   print(f"У {device} {intf} ошибка {e.error}")

if __name__ == "__main__":
   device_list = []
   intf_dict = {}
   with open("results/mikrotik/intf_info/all_devices.yaml") as f:
        intf_info = yaml.safe_load(f)
   for device in intf_info:
       device_list.append(device)
       intf_list = []
       for line in intf_info[device]:
           intf_list.append(line)
       intf_dict[device] = intf_list
   intf_add(device_list, intf_dict, intf_info)
