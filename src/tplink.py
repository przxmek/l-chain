from pyHS100 import SmartPlug
import json
import hashlib

def tplink_hash(ip):
    plug = SmartPlug(ip)

    pluginfo = json.loads(str(json.dumps(plug.hw_info)))

    plughash = hashlib.sha1()
    plughash.update(pluginfo['hwId'].encode())

    hash_s = "0x" + plughash.hexdigest() + "862ba9e16088902221101976"

    return hash_s

# print(tplink_hash("192.168.1.226"))
