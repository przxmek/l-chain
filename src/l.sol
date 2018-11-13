pragma solidity ^0.4.24;

contract L {
    address public owner;

    mapping(address => address) socketToDevices;

    mapping(address => uint) prices;

    event PowerDelivery(address indexed from, address sokcetId, address deviceId, uint consumedEnergy, uint pricePerUnit);
    event SocketUpdate(address indexed from, address socketId, address deviceId);

    constructor() public {
        owner = msg.sender;
    }


    // Private methods

    function isNotNullAddress(address addr) internal pure returns (bool) {
        return !(addr == address(0));
    }


    // Public const (view) methods

    function getPriceForDevice(address deviceId) public view returns (uint) {
        uint saved_price = prices[deviceId];
        return saved_price;
    }

    function getDeviceForSocket(address socketId) public view returns (address) {
        require(isNotNullAddress(socketId));
        return socketToDevices[socketId];
    }

    // Checks if a device plugged in a given socket is authorized to use it.
    function isDeviceAuthorized(address socketId) public view returns (bool) {
        // Get device ID
        address deviceId = socketToDevices[socketId];
        require(isNotNullAddress(deviceId), "No device plugged to socket");

        // Check if device is allowed for this socket
        // require(allowedDevices[socketId].contains(deviceId));

        return true;
    }


    // Public functions (transactions)

    function socketUpdate(address socketId, address deviceId) public returns (bool)  {
        socketToDevices[socketId] = deviceId;
        emit SocketUpdate(msg.sender, socketId, deviceId);
        return true;
    }

    function powerDelivery(address socketId, uint consumedEnergy) public {
        // Check if socketId is not empty
        require(isNotNullAddress(socketId));

        // TODO check if msg.sender (L-BOX) is a registered L-BOX

        // TODO Check if Socket ID is a registered socket ID
        require(isDeviceAuthorized(socketId), "Unauthorized device plugged to socket");

        // Get device ID
        address deviceId = socketToDevices[socketId];

        // Get private for electricity
        uint price = getPriceForDevice(deviceId);

        emit PowerDelivery(msg.sender, socketId, deviceId, consumedEnergy, price);
    }
}