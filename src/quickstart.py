import subprocess

import web3
from web3.auto import w3


def program():
    if not w3.isConnected():
        raise Exception("Could not connect to the node")

    contract_abi = '[{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"total","type":"uint256"}],"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"}]'
    contract_address = "0xEBB940F4AC07A5c84A5F145D21db662297e00fE4"

    test_account_address = '0x005399d04E229bFD42BEAf91570689AC9491c1B6'
    test_account_password = 'test'

    another_account_address = '0x0095efEDD680CDf61Ab2a60ED1D96EFc85181566'

    w3.personal.unlockAccount(test_account_address, test_account_password)

    # Instantiate contract
    # Create the contract instance with the newly-deployed address
    ltoken = w3.eth.contract(
        address=contract_address,
        abi=contract_abi,
    )


    result = ltoken.functions.transfer(to=another_account_address, value=42).transact({'from': test_account_address})
    print(result.hex())

    # Getters + Setters for web3.eth.contract object
    # print('Contract value: {}'.format(contract_instance.greet()))
    # contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
    # print('Setting value to: Nihao')
    # print('Contract value: {}'.format(contract_instance.greet()))



if __name__ == '__main__':
    subprocess.call(["bash", "config.sh"])
    program()