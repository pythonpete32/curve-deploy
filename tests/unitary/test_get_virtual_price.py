import pytest

from tests.conftest import PRECISIONS

INITIAL_AMOUNTS = [10**(i+6) for i in PRECISIONS]


@pytest.fixture(scope="module", autouse=True)
def setup(alice, aave_coins, swap):
    for coin, amount in zip(aave_coins, INITIAL_AMOUNTS):
        coin._mint_for_testing(alice, amount, {'from': alice})
        coin.approve(swap, 2**256-1, {'from': alice})

    swap.add_liquidity(INITIAL_AMOUNTS, 0, {'from': alice})


def test_initial(swap):
    assert swap.get_virtual_price() == 10**18


@pytest.mark.parametrize("idx", range(len(INITIAL_AMOUNTS)))
def test_increase_one_coin(alice, swap, aave_coins, idx):
    aave_coins[idx]._mint_for_testing(swap, INITIAL_AMOUNTS[idx]*3, {'from': alice})

    assert 0.999 < swap.get_virtual_price() / (2 * 10**18) < 1


def test_increase_all_coins(alice, swap, aave_coins):
    for i, coin in enumerate(aave_coins):
        coin._mint_for_testing(swap, INITIAL_AMOUNTS[i], {'from': alice})

    assert swap.get_virtual_price() == 2 * 10**18
