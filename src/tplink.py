from pyHS100 import SmartPlug
import json
import hashlib


def tplink_hash(ip):
    plug = SmartPlug(ip)
    # read hw information und parse JSON
    pluginfo = json.loads(str(json.dumps(plug.hw_info)))
    # hash
    plughash = hashlib.sha1()
    # hash hw id
    plughash.update(pluginfo['hwId'].encode())
    # build hash for ETH
    hash_s = "0x" + plughash.hexdigest() + "862ba9e16088902221101976"
    # return hash
    return hash_s


def tplink_consumption(ip):
    plug = SmartPlug(ip)
    # read meter information und parse JSON
    pluginfo = json.loads(str(json.dumps(plug.get_emeter_realtime())))
    # filter for total power consumption
    consumption = pluginfo['total']
    # return consumption
    return consumption

# print(tplink_hash("192.168.1.226"))
print(tplink_consumption("192.168.1.226"))