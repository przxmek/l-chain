pragma solidity ^0.4.24;

contract L {
    address public owner;

    mapping(string => string) socketToDevices;

    mapping(string => uint) prices;

    event PowerDelivery(address indexed from, string sokcetId, string deviceId, uint consumedEnergy, uint pricePerUnit);
    event SocketUpdate(address indexed from, string socketId, string deviceId);

    constructor() public {
        owner = msg.sender;
    }


    // Private methods

    function isNotEmptyString(string str) internal pure returns (bool) {
        return (bytes(str).length != 0);
    }


    // Public const (view) methods

    function getPriceForDevice(string deviceId) public view returns (uint) {
        uint saved_price = prices[deviceId];
        return saved_price;
    }

    function getDeviceForSocket(string socketId) public view returns (string) {
        require(isNotEmptyString(socketId));
        return socketToDevices[socketId];
    }

    // Checks if a device plugged in a given socket is authorized to use it.
    function isDeviceAuthorized(string socketId) public view returns (bool) {
        // Get device ID
        string storage deviceId = socketToDevices[socketId];
        require(isNotEmptyString(deviceId), "No device plugged to socket");

        // Check if device is allowed for this socket
        // require(allowedDevices[socketId].contains(deviceId));

        return true;
    }


    // Public functions (transactions)

    function socketUpdate(string socketId, string deviceId) public returns (bool)  {
        socketToDevices[socketId] = deviceId;
        emit SocketUpdate(msg.sender, socketId, deviceId);
        return true;
    }

    function powerDelivery(string socketId, uint consumedEnergy) public {
        // Check if socketId is not empty
        require(isNotEmptyString(socketId));

        // TODO check if msg.sender (L-BOX) is a registered L-BOX

        // TODO Check if Socket ID is a registered socket ID
        require(isDeviceAuthorized(socketId), "Unauthorized device plugged to socket");

        // Get device ID
        string storage deviceId = socketToDevices[socketId];

        // Get private for electricity
        uint price = getPriceForDevice(deviceId);

        emit PowerDelivery(msg.sender, socketId, deviceId, consumedEnergy, price);
    }
}