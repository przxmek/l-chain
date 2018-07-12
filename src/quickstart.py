import subprocess

subprocess.call(["bash", "config.sh"])

from web3.auto import w3

print (w3.eth.blockNumber)