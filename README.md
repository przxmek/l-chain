# Installing Parity Wallet on Raspberry-PI

1. Download Parity 10.6
2. Install it with `dpkg`

        $ sudo dpkg --ignore-depends=libssl1.0.0 -i parity_1.11.6_ubuntu_armhf.deb

3. Prepare config files
  
  - `stromdao_lgruppe.conf`
  - `stromdao_poa_spec.json`
  - echo "TEST" >> pwd_file

4. Initial startup
    4.1 Disable mining options from `stromdao_lgruppe.conf`
    4.2 Enable SSH Forwarding
    4.3 Start parity `parity -c stromdao_lgruppe.conf ui`
    4.4 Create Authority account, write down address and recovery phrase
    4.5 Update `stromdao_lgruppe.conf` & `stromdao_poa_spec.json` with address of authority node
    4.6 Update `pwd_file` with the password for authority node

5. Clean up
    5.1 Restart parity
    5.2 Enjoy


#### SSH Tunneling ports

    $ ssh pi@172.16.50.137 -L 8080:localhost:8080 -L 8180:localhost:8180 -L 8546:localhost:8546 -L 8545:localhost:8545