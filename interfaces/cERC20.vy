# Interface for the used methods in Compound cERC20
#
# Events

event Transfer:
    _from: indexed(address)
    _to: indexed(address)
    _value: uint256

event Approval:
    _owner: indexed(address)
    _spender: indexed(address)
    _value: uint256

# Functions

@view
@external
def totalSupply() -> uint256:
    pass

@view
@external
def allowance(_owner: address, _spender: address) -> uint256:
    pass

@external
def transfer(_to: address, _value: uint256) -> bool:
    pass

@external
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    pass

@external
def approve(_spender: address, _value: uint256) -> bool:
    pass

@external
def burn(_value: uint256):
    pass

@external
def burnFrom(_to: address, _value: uint256):
    pass

@view
@external
def name() -> String[64]:
    pass

@view
@external
def symbol() -> String[32]:
    pass

@view
@external
def decimals() -> uint256:
    pass

@view
@external
def balanceOf(arg0: address) -> uint256:
    pass

@external
def mint(mintAmount: uint256) -> uint256:
    """
     @notice Sender supplies assets into the market and receives cTokens in exchange
     @dev Accrues interest whether or not the operation succeeds, unless reverted
     @param mintAmount The amount of the underlying asset to supply
     @return uint 0=success, otherwise a failure (see ErrorReporter.sol for details)
    """
    pass

@external
def redeem(redeemTokens: uint256) -> uint256:
    """
     @notice Sender redeems cTokens in exchange for the underlying asset
     @dev Accrues interest whether or not the operation succeeds, unless reverted
     @param redeemTokens The number of cTokens to redeem into underlying
     @return uint 0=success, otherwise a failure (see ErrorReporter.sol for details)
    """
    pass

@external
def redeemUnderlying(redeemAmount: uint256) -> uint256:
    """
     @notice Sender redeems cTokens in exchange for a specified amount of underlying asset
     @dev Accrues interest whether or not the operation succeeds, unless reverted
     @param redeemAmount The amount of underlying to redeem
     @return uint 0=success, otherwise a failure (see ErrorReporter.sol for details)
    """
    pass

@view
@external
def exchangeRateStored() -> uint256:
    """
     @notice Calculates the exchange rate from the underlying to the CToken
     @dev This function does not accrue interest before calculating the exchange rate
     @return Calculated exchange rate scaled by 1e18
    """
    pass

@external
def exchangeRateCurrent() -> uint256:
    """
     * @notice Accrue interest then return the up-to-date exchange rate
     * @return Calculated exchange rate scaled by 1e18
    """
    pass

@external
@view
def supplyRatePerBlock() -> uint256:
    pass

@external
@view
def accrualBlockNumber() -> uint256:
    pass
