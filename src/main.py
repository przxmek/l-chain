# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 16:25:27 2018

@author: BoehmCh
"""

import json
import uuid
#import sys
#from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler
import nfc
from blockchain import LBlockchain
import homematic
import _thread

testJson = '{"uuid-device": "0xA2 0xD4 0x92 0x30", "uuid-socket" : "b53aede2-2f6a-4a11-9e02-6237301a100f"}'
testJson2 = '{"uuid-device": "0xA2 0xD4 0x92 0x29", "uuid-socket" : "d042a319-6fd5-41d5-b9a5-4f59b56c920e"}'

idMap = {
    'b53aede2-2f6a-4a11-9e02-6237301a100f': {
        'billingId': '1585',
        'switchId': '1530',
    },
    'd042a319-6fd5-41d5-b9a5-4f59b56c920e': {
        'billingId': '1585',
        'switchId': '1530',
    },
    'fbc8b32e-a60c-4d5e-ab04-1229803879a7': {
        'billingId': '1585',
        'switchId': '1580',
    },
    'dfd3794d-581e-4992-bacc-7670a37bdcfe': {
        'billingId': '1585',
        'switchId': '1530',
    },
    '230b53fb-c5ed-4af4-b448-f9222d656482': {
        'billingId': '1635',
        'switchId': '1467',
    }
}

billingLimit = 20

#x = json.loads(testJson)
#print(x)

#testDevice = json.loads("0xA2 0xD4 0x92 0x30")
#testSocket = json.loads("b53aede2-2f6a-4a11-9e02-6237301a100f")

lblockchain = LBlockchain()

class Socket:
    def __init__(self, nfcJson, inLastSocketPower):
        self.socketId = nfcJson['uid_socket']
        self.homematicBillingId = idMap[str(self.socketId)]['billingId']
        self.homematicSwitchId = idMap[str(self.socketId)]['switchId']
        self.deviceId = nfcJson['uid_device']
        self.lastBillingPower = inLastSocketPower
        self.plugged = False
        if self.deviceId != 0:
            self.plugged = True
            
    def setLastBillingPower(self, value):
        delta = value - self.lastBillingPower
        lblockchain.powerDelivery(self.socketId, int(delta))
        self.lastBillingPower = value

    def socketUpdate(self, deviceId):
        print("socketUpdate socket:" + str(self.socketId) + " device: " + str(deviceId))
        lblockchain.updateSocket(self.socketId, deviceId)

    def getLastBillingPower(self):
        return self.lastBillingPower
    
    def getDeviceId(self):
        return self.deviceId

def socketUpdateCallback(nfcJson):
    print("JSON: " + str(nfcJson))
    socketId = nfcJson['uid_socket']
    deviceId = nfcJson['uid_device']

    # Skipping disconnected sockets
    if deviceId == '0x01 0x00 0x00 0x00 0x00 0x00 0x00':
        return

    for socket in sockets:
        if socket.socketId == socketId:
            socket.socketUpdate(deviceId)
            return

    # Create new socket
    print("Creating new socket: " + socketId)
    socket = Socket(nfcJson, 0)
    sockets.append(socket)
    socket.socketUpdate(deviceId)

sockets = []

#socket = next((socket for socket in sockets if socket.socketId == uuid.UUID('b53aede2-2f6a-4a11-9e02-6237301a100f')), None)
#print(socket.socketId)

def loop():
    print("LOOP sockets count" + str(len(sockets)))
    for socket in sockets:
        print(str(socket))
        if (socket.getDeviceId != 0):
            print("read powerConsumption from HomeMatic")

            #request Homematic
            currentPowerConsumption = float(homematic.get_power_consumption(socket))

            if ((currentPowerConsumption - socket.getLastBillingPower()) > billingLimit):
                print("update blockchain")
                #update blockchain
                socket.setLastBillingPower(currentPowerConsumption)
            else:
                print("do nothing...")


# def nfc_thread():
#     nfc.init_nfc(socketUpdateCallback)


if __name__ == '__main__':
    sched = BlockingScheduler()

    _thread.start_new_thread(nfc.init_nfc, (socketUpdateCallback,))

    sched.add_job(loop, "interval", seconds=2)
    sched.start()
