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


@pytest.mark.parametrize("min_amount", [INITIAL_AMOUNTS, [0, 0, 0]])
def test_remove_liquidity(alice, swap, aave_coins, pool_token, min_amount):
    swap.remove_liquidity(3 * 10**24, min_amount, {'from': alice})

    for coin, amount in zip(aave_coins, INITIAL_AMOUNTS):
        assert coin.balanceOf(alice) == amount
        assert coin.balanceOf(swap) == 0

    assert pool_token.balanceOf(alice) == 0
    assert pool_token.totalSupply() == 0


def test_remove_partial(alice, swap, aave_coins, pool_token):
    withdraw_amount = 6 * 10**23
    swap.remove_liquidity(withdraw_amount, [0, 0, 0], {'from': alice})

    for coin, amount in zip(aave_coins, INITIAL_AMOUNTS):
        pool_balance = coin.balanceOf(swap)
        alice_balance = coin.balanceOf(alice)
        assert alice_balance * 4 == pool_balance
        assert alice_balance + pool_balance == amount

    assert pool_token.balanceOf(alice) == 3 * 10**24 - withdraw_amount
    assert pool_token.totalSupply() == 3 * 10**24 - withdraw_amount


@pytest.mark.parametrize("idx", range(len(INITIAL_AMOUNTS)))
def test_below_min_amount(alice, swap, aave_coins, pool_token, idx):
    min_amount = INITIAL_AMOUNTS.copy()
    min_amount[idx] += 1

    with brownie.reverts("Withdrawal resulted in fewer coins than expected"):
        swap.remove_liquidity(3 * 10**24, min_amount, {'from': alice})


def test_amount_exceeds_balance(alice, swap, aave_coins, pool_token):
    with brownie.reverts("dev: insufficient funds"):
        swap.remove_liquidity(3 * 10**24 + 1, [0, 0, 0], {'from': alice})


@pytest.mark.parametrize("min_amount", [INITIAL_AMOUNTS, [0, 0, 0]])
def test_increased_a_token_balance(alice, swap, aave_coins, pool_token, min_amount):
    for i, coin in enumerate(aave_coins):
        coin._mint_for_testing(swap, INITIAL_AMOUNTS[i], {'from': alice})

    swap.remove_liquidity(3 * 10**24, min_amount, {'from': alice})

    for coin, amount in zip(aave_coins, INITIAL_AMOUNTS):
        assert coin.balanceOf(alice) == amount * 2
        assert coin.balanceOf(swap) == 0
