pragma solidity ^0.5.0;


library SafeMath {
    function add(uint a, uint b) internal pure returns (uint c) {
        c = a + b;
        require(c >= a); // dev: overflow
    }
    function sub(uint a, uint b) internal pure returns (uint c) {
        require(b <= a); // dev: underflow
        c = a - b;
    }
    function mul(uint a, uint b) internal pure returns (uint c) {
        c = a * b;
        require(a == 0 || c / a == b); // dev: overflow
    }
    function div(uint a, uint b) internal pure returns (uint c) {
        require(b > 0); // dev: divide by zero
        c = a / b;
    }
}


contract AaveLendingPoolMock {

    using SafeMath for uint256;

    /**
    * @dev deposits The underlying asset into the reserve. A corresponding amount
           of the overlying asset (aTokens) is minted.
    * @param _reserve the address of the reserve
    * @param _amount the amount to be deposited
    * @param _referralCode integrators are assigned a referral code and can potentially receive rewards.
    **/
    function deposit(address _reserve, uint256 _amount, uint16 _referralCode) external payable {

    }

}
