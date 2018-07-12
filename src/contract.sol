pragma solidity ^0.4.24;


/**
 * @title ERC20Basic
 * @dev Simpler version of ERC20 interface
 * @dev see https://github.com/ethereum/EIPs/issues/179
 */
contract ERC20Basic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}

contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender)
    public view returns (uint256);

  function transferFrom(address from, address to, uint256 value)
    public returns (bool);

  function approve(address spender, uint256 value) public returns (bool);
  event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
  );
}

contract IssueableToken is ERC20Basic {

  mapping(address => uint256) balances;

  uint256 public totalSupply_;
  address public owner;

  constructor() public {
	  owner=msg.sender;
  }
  /**
  * @dev total number of tokens in existence
  */
  function totalSupply() public view returns (uint256) {
    return totalSupply_;
  }


  /**
  * @dev transfer token for a specified address
  * @param _to The address to transfer to.
  * @param _value The amount to be transferred.
  */
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    if(msg.sender==owner) {
       totalSupply_+=_value;
	   balances[_to]+=_value;
    } else {
        require(_value <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender]-_value;
        balances[_to] = balances[_to] + _value;
    }
    emit Transfer(msg.sender, _to, _value);
    return true;
  }

  /**
  * @dev Gets the balance of the specified address.
  * @param _address The address to query the the balance of.
  * @return An uint256 representing the amount owned by the passed address.
  */
  function balanceOf(address _address) public view returns (uint256) {
    return balances[_address];
  }

  function setOwner(address _owner) public {
	  if(msg.sender!=owner) revert();
	  owner=_owner;
   }
}

contract TokenFactory {
		 event Built(address indexed _token);
		function buildToken() public returns (IssueableToken) {
			IssueableToken token = new IssueableToken();
			token.setOwner(msg.sender);
			emit Built(token);
		return token;
		}
}

