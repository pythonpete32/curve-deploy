import brownie
import pytest

from tests.conftest import PRECISIONS

INITIAL_AMOUNTS = [10**(i+6) for i in PRECISIONS]


@pytest.fixture(scope="module", autouse=True)
def setup(alice, aave_coins, swap):
    for coin, amount in zip(aave_coins, INITIAL_AMOUNTS):
        coin._mint_for_testing(alice, amount, {'from': alice})
        coin.approve(swap, 2**256-1, {'from': alice})

    swap.add_liquidity(INITIAL_AMOUNTS, 0, {'from': alice})


@pytest.mark.parametrize("divisor", [1, 2, 10])
def test_remove_liquidity_balanced(alice, swap, aave_coins, pool_token, divisor):
    amounts = [i // divisor for i in INITIAL_AMOUNTS]
    max_burn = (3 * 10**24) // divisor
    swap.remove_liquidity_imbalance(amounts, max_burn, {'from': alice})

    for i, coin in enumerate(aave_coins):
        assert coin.balanceOf(alice) == amounts[i]
        assert coin.balanceOf(swap) == INITIAL_AMOUNTS[i] - amounts[i]

    assert pool_token.balanceOf(alice) == (3 * 10**24) - max_burn
    assert pool_token.totalSupply() == (3 * 10**24) - max_burn


@pytest.mark.parametrize("idx", range(len(PRECISIONS)))
def test_remove_two_coins(alice, swap, aave_coins, pool_token, idx):
    amounts = [i//2 for i in INITIAL_AMOUNTS]
    amounts[idx] = 0

    swap.remove_liquidity_imbalance(amounts, 3*10**24, {'from': alice})

    for i, coin in enumerate(aave_coins):
        assert coin.balanceOf(alice) == amounts[i]
        assert coin.balanceOf(swap) == INITIAL_AMOUNTS[i] - amounts[i]

    actual_balance = pool_token.balanceOf(alice)
    actual_total_supply = pool_token.totalSupply()

    ideal_balance = 2 * 10**24
    assert actual_balance == actual_total_supply
    assert ideal_balance * 0.99 < actual_balance < ideal_balance


@pytest.mark.xfail(reason="rounding issues")
@pytest.mark.parametrize("idx", range(len(PRECISIONS)))
def test_remove_one_coin(alice, swap, aave_coins, pool_token, idx):
    burn_amount = (3 * 10**24) // 2
    expected = swap.calc_withdraw_one_coin(burn_amount, idx)

    amounts = [0, 0, 0]
    amounts[idx] = expected

    swap.remove_liquidity_imbalance(amounts, 3*10**24, {'from': alice})

    assert aave_coins[idx].balanceOf(alice) == expected
    assert pool_token.balanceOf(alice) == burn_amount


@pytest.mark.parametrize("divisor", [1, 2, 10])
def test_exceeds_max_burn(alice, swap, aave_coins, pool_token, divisor):
    amounts = [i // divisor for i in INITIAL_AMOUNTS]
    max_burn = (3 * 10**24) // divisor

    with brownie.reverts("Slippage screwed you"):
        swap.remove_liquidity_imbalance(amounts, max_burn-1, {'from': alice})


def test_cannot_remove_zero(alice, swap):
    with brownie.reverts("dev: zero tokens burned"):
        swap.remove_liquidity_imbalance([0, 0, 0], 0, {'from': alice})


def test_no_totalsupply(alice, swap):
    swap.remove_liquidity_imbalance(INITIAL_AMOUNTS, 2**256-1, {'from': alice})
    with brownie.reverts("dev: zero total supply"):
        swap.remove_liquidity_imbalance([0, 0, 0], 0, {'from': alice})
