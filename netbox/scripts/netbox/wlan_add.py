import yaml
import pynetbox
import requests
from pprint import pprint

def wlan_add(devices):
    nb = pynetbox.api("https://netbox/", token="token")
    session = requests.Session()
    session.verify = False
    nb.http_session = session
    with open("results/unifi/wifi_info/all_wlans.yaml") as f:
        wlans = yaml.safe_load(f)
    for device in devices:
        params = wlans[device]
        for param in params:
            try:
               vlan = param['vlan']
               vlan_id = nb.ipam.vlans.get(vid=vlan)
               param['vlan'] = vlan_id.id                      
            except: pass        
            try:
               nb.wireless.wireless_lans.create(param)
            except pynetbox.core.query.RequestError as e:
               print(f"У {device} ошибка {e.error}")

if __name__ == "__main__":
    with open("results/unifi/wifi_info/all_wlans.yaml") as f:
        devices = yaml.safe_load(f)
    wlan_add(devices)
