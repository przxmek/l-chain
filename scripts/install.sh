#!/bin/bash

# Install git
which git 2>&1 > /dev/null || (sudo apt update && sudo apt install git)


# Clone the repo
# NOTE: If repo is private configure your ssh key
# git clone git@github.com:przxmek/l-chain.git l-chain

# Install Parity client
source ./get-parity.sh -r stable
