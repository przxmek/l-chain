#!/bin/bash

INSTALL_PATH=`pwd`
LCHAIN_PATH=/opt/lchain
CONF_PATH=${LCHAIN_PATH}/conf

SIGNER_PWD="lchain"
ENGINE_SIGNER="0x0"

sudo mkdir -p ${LCHAIN_PATH}
sudo mkdir -p ${CONF_PATH}


configure_lchain_user () {
	id -u lchain 2>&1 > /dev/null || (sudo adduser --system --no-create-home --disabled-password --disabled-login --group lchain)
	sudo chown -R lchain ${LCHAIN_PATH}
	sudo chgrp -R lchain ${LCHAIN_PATH}
}


install_daemon () {
    sudo cp ${INSTALL_PATH}/install-files/lchain.service /etc/systemd/system/lchain.service

    sudo systemctl enable lchain
    sudo systemctl start lchain
}


update_configs () {
cat <<EOF | sudo tee ${CONF_PATH}/lchain.conf > /dev/null
[parity]
# Lchain network
chain = "${CONF_PATH}/lchain-poa-spec.json"
# Blockchain and settings will be stored in ${LCHAIN_PATH}.
base_path = "${LCHAIN_PATH}/privatechain"
keys_path = "${LCHAIN_PATH}/keys"
# Experimental: run in light client mode. Light clients synchronize a bare minimum of data and fetch necessary data on-demand from the network. Much lower in storage, potentially higher in bandwidth. Has no effect with subcommands.
light = true

[account]
# File at pwd_file should contain passwords to unlock your accounts. One password per line.
password  = ["pwd_file"]

[ui]
#  Wallet will listen for connections on IP 0.0.0.0.
interface = "0.0.0.0" # Only for development!!!
# List of allowed Host header values. This option will validate the Host header sent by the browser, it is additional security against some attack vectors. Special options: "all", "none",.
hosts = ["all"] # Only for development!!!

[network]
port = 30400
#bootnodes = [
#"enode://a2da77cc4af04812324a99b9479d5bb1db228afcd5114447e23baa2c648459abb03e09cac115b33086809ba333788ca69597ace50b6588e3956ef2432c811c18@108.61.210.201:30400",
#"enode://4a8eae0658832ddad97a55b546c23c71e2123f23643367d8570cfce9676807658d7b83a2fb62524e3762840b7e6c016d84afe6d53c3941ebb9402775dd44ca06@45.32.155.49:30400",
#"enode://6049758d7e6071c3b9d80ae0b5af5952f2f004a44055f1c5ef3991a3f8dd3d7b29d595b1499b4fd8ada8be20b5c2604d4f7bac0939e14edd69abbfeb20cd9af6@62.75.168.184:30400"
#]

# reserved_peers = "lchain_peers.txt"

[rpc]
#  JSON-RPC will be listening for connections on IP 0.0.0.0.
interface = "0.0.0.0" # Only for development!!!
# Allows Cross-Origin Requests from domain '*'.
cors = ["*"] # Only for development!!!
apis = ["web3", "eth", "net", "personal", "parity", "parity_set", "traces", "rpc", "parity_accounts"]

[websockets]
#  JSON-RPC will be listening for connections on IP 0.0.0.0.
interface = "0.0.0.0" # Only for development!!!

[dapps]
# path = "${LCHAIN_PATH}/dapps/"

[mining]
engine_signer = "${ENGINE_SIGNER}"
reseal_on_txs = "none"
usd_per_tx = "0"
EOF


cat <<EOF | sudo tee ${CONF_PATH}/lchain-poa-spec.json > /dev/null
{
    "name": "L-Chain",
    "engine": {
		"authorityRound": {
			"params": {
			"stepDuration": "4",
			"validators": {
				"list": [
				"0x0013c31077fc1b0cb73a677f3b587aaeb5e07ffb",
				"0x0075D14a828F22584f69B2F4cDce6877D5Bcbf7c",
				"0xd87064f2ca9bb2ec333d4a0b02011afdf39c4fb0",
				"0xfa21fb716322ee4ebbec6aefb9208a428e0b56f4",
                                "0x007402E0F3950493d26c39eA56BbF8D11FD68e30"
				]
			}}
		}
	},
    "params": {
        "maximumExtraDataSize": "0x20",
	    "gasLimitBoundDivisor": "0x400",
        "minGasLimit": "0x1388",
        "networkID" : "0x3"
    },
    "genesis": {
		"seal": {
			"authorityRound": {
				"step": "0x0",
				"signature": "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
			}
		},
        "difficulty": "0x20",
        "gasLimit": "0xFF5B8D80",
		"author": "0x0000000000000000000000000000000000000000",
		"timestamp": "0x00",
		"parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
		"extraData": "0x"
    },
    "accounts": {
        "0x0000000000000000000000000000000000000001": { "balance": "1", "builtin": { "name": "ecrecover", "pricing": { "linear": { "base": 3000, "word": 0 } } } },
        "0x0000000000000000000000000000000000000002": { "balance": "1", "builtin": { "name": "sha256", "pricing": { "linear": { "base": 60, "word": 12 } } } },
        "0x0000000000000000000000000000000000000003": { "balance": "1", "builtin": { "name": "ripemd160", "pricing": { "linear": { "base": 600, "word": 120 } } } },
        "0x0000000000000000000000000000000000000004": { "balance": "1", "builtin": { "name": "identity", "pricing": { "linear": { "base": 15, "word": 3 } } } }
    }
}
EOF
}

update_configs

echo "$SIGNER_PWD" | sudo tee ${CONF_PATH}/pwd_file > /dev/null

cd ${LCHAIN_PATH}

ENGINE_SIGNER=`sudo parity -c ${CONF_PATH}/lchain.conf account new`

update_configs

configure_lchain_user
install_daemon
