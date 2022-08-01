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
               intf_nb = nb.dcim.interfaces.get(name=intf, device=device)
               try:
                   params['address'] = intf_info[device][intf]['address']
                   params['status'] = 'active'
                   params['assigned_object_type'] = "dcim.interface" 
                   params['assigned_object_id'] = intf_nb.id
               except: continue 
               try:
                   params['role'] = intf_info[device][intf]['role']
               except: pass
               try:
                   nb.ipam.ip_addresses.create(params)
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
