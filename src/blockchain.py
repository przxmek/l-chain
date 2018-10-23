import subprocess

import web3
from web3.auto import w3


def _load_config():
    subprocess.call(["bash", "config.sh"])


def _check_connection():
    if not w3.isConnected():
        raise Exception("Could not connect to the node", '')


class LBlockchain:
    def __init__(self):
        _check_connection()

        contract_address = '0x7a96ebe9c9e85600c3bd87827cff5bFAe253c1AE'
        contract_abi = '[{"constant":true,"inputs":[{"name":"socketId","type":"string"}],"name":"isDeviceAuthorized","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"socketId","type":"string"}],"name":"getDeviceForSocket","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"socketId","type":"string"},{"name":"deviceId","type":"string"}],"name":"socketUpdate","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"deviceId","type":"string"}],"name":"getPriceForDevice","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"socketId","type":"string"},{"name":"consumedEnergy","type":"uint256"}],"name":"powerDelivery","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":false,"name":"sokcetId","type":"string"},{"indexed":false,"name":"deviceId","type":"string"},{"indexed":false,"name":"consumedEnergy","type":"uint256"},{"indexed":false,"name":"pricePerUnit","type":"uint256"}],"name":"PowerDelivery","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":false,"name":"socketId","type":"string"},{"indexed":false,"name":"deviceId","type":"string"}],"name":"SocketUpdate","type":"event"}]'
        self.l = w3.eth.contract(
            address=contract_address,
            abi=contract_abi,
        )

        # Recovery phrase: cytoplast talon roundness escargot wrath idly prewar whoops unlearned sarcasm deplete monogamy
        # self.account_addr = '0x00eB790E8A800fdF1288DBaCCC443e4578687E8F'
        # self.account_pwd = 'lbox'
        self.account_addr = '0x0029E01550F56456403222350D3D396bE30002B4'
        self.account_pwd = 'test'

        self._authorize()

    def _authorize(self):
        res = w3.personal.unlockAccount(self.account_addr, self.account_pwd)
        print('auth result: ' + str(res))

    def updateSocket(self, socketId, deviceId):
        self._authorize()
        return self.l.functions.socketUpdate(socketId, deviceId).transact({'from': self.account_addr})

    def powerDelivery(self, socketId, consumedEnergy):
        self._authorize()
        return self.l.functions.powerDelivery(socketId, consumedEnergy).transact({'from': self.account_addr})

    def isDeviceAuthorized(self, socketId):
        return self.l.functions.isDeviceAuthorized(socketId).call()

    def getPriceForDevice(self, socketId):
        return self.l.functions.getPriceForDevice(socketId).call()

    def getDeviceForSocket(self, socketId):
        return self.l.functions.getDeviceForSocket(socketId).call()


if __name__ == '__main__':
    _load_config()

    l = LBlockchain()


    # l.isDeviceAuthorized('socketId')
    # print(l.updateSocket('socket2', 'boiler').hex())
    # print(l.powerDelivery('socket2', 42).hex())
    # print(l.getDeviceForSocket('socket2'))
    # print(l.getPriceForDevice('socket2'))
    # print(l.isDeviceAuthorized('socket2'))



