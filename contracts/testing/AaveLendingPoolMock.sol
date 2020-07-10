pragma solidity ^0.5.0;

import "./ATokenMock.sol";


contract AaveLendingPoolMock {

    uint16 public lastReferral;

    mapping (address => address) aTokens;

    function deployToken(string calldata _name, string calldata _symbol, address _underlying) external returns (ATokenMock) {
        ATokenMock _aToken = new ATokenMock(_name, _symbol, _underlying);
        aTokens[_underlying] = address(_aToken);
        return _aToken;
    }

    /**
    * @dev deposits The underlying asset into the reserve. A corresponding amount
           of the overlying asset (aTokens) is minted.
    * @param _reserve the address of the reserve
    * @param _amount the amount to be deposited
    * @param _referralCode integrators are assigned a referral code and can potentially receive rewards.
    **/
    function deposit(address _reserve, uint256 _amount, uint16 _referralCode) external payable {
        require (aTokens[_reserve] != address(0));
        lastReferral = _referralCode;
        IERC20(_reserve).transferFrom(msg.sender, aTokens[_reserve], _amount);
    }

}
