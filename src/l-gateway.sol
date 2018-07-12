pragma solidity ^0.4.24;

contract LGateway {
    address public currentVersion;
    address public owner;

    function LGateway(address initAddr){
        currentVersion = initAddr;
        owner = msg.sender;
    }

    function update(address newAddress){
        if(msg.sender != owner) throw;
        currentVersion = newAddress;
    }

    function(){
        if(!currentVersion.delegatecall(msg.data)) throw;
    }
}