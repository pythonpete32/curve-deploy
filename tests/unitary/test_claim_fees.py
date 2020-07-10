import itertools

import brownie
import pytest

from tests.conftest import PRECISIONS

INITIAL_AMOUNTS = [10**(i+6) for i in PRECISIONS]
MAX_FEE = 5 * 10**9


@pytest.fixture(scope="module", autouse=True)
def setup(rpc, alice, bob, aave_coins, swap):
    for coin, amount in zip(aave_coins, INITIAL_AMOUNTS):
        coin._mint_for_testing(alice, amount, {'from': alice})
        coin._mint_for_testing(bob, amount, {'from': bob})
        coin.approve(swap, 2**256-1, {'from': alice})
        coin.approve(swap, 2**256-1, {'from': bob})

    swap.add_liquidity(INITIAL_AMOUNTS, 0, {'from': alice})

    swap.commit_new_fee(MAX_FEE, MAX_FEE, 0, {'from': alice})
    rpc.sleep(86400*3)
    swap.apply_new_fee({'from': alice})


def test_admin_balances(alice, bob, swap, aave_coins):
    for send, recv in [(0, 1), (1, 2), (2, 0)]:
        swap.exchange(send, recv, INITIAL_AMOUNTS[send], 0, {'from': bob})

    for i in range(3):
        admin_fee = swap.admin_balances(i)
        assert admin_fee > 0
        assert admin_fee + swap.balances(i) == aave_coins[i].balanceOf(swap)


@pytest.mark.parametrize("sending,receiving,other", itertools.permutations([0, 1, 2], 3))
def test_withdraw_one_coin(alice, bob, swap, aave_coins, sending, receiving, other):
    swap.exchange(sending, receiving, INITIAL_AMOUNTS[sending], 0, {'from': bob})

    admin_fee = swap.admin_balances(receiving)
    assert admin_fee > 0

    assert swap.admin_balances(sending) == 0
    assert swap.admin_balances(other) == 0

    swap.withdraw_admin_fees({'from': alice})
    assert aave_coins[receiving].balanceOf(alice) == admin_fee
    assert swap.admin_balances(receiving) == 0


def test_withdraw_all_coins(alice, bob, swap, aave_coins):
    for send, recv in [(0, 1), (1, 2), (2, 0)]:
        swap.exchange(send, recv, INITIAL_AMOUNTS[send], 0, {'from': bob})

    admin_fees = [swap.admin_balances(i) for i in range(3)]

    swap.withdraw_admin_fees({'from': alice})
    balances = [i.balanceOf(alice) for i in aave_coins]

    assert admin_fees == balances


def test_withdraw_only_owner(bob, swap):
    with brownie.reverts("dev: only owner"):
        swap.donate_admin_fees({'from': bob})


def test_donate(alice, bob, swap, aave_coins):
    for send, recv in [(0, 1), (1, 2), (2, 0)]:
        swap.exchange(send, recv, INITIAL_AMOUNTS[send], 0, {'from': bob})

    swap.donate_admin_fees({'from': alice})

    assert [swap.admin_balances(i) for i in range(3)] == [0, 0, 0]
    assert [i.balanceOf(alice) for i in aave_coins] == [0, 0, 0]


def test_donate_only_owner(bob, swap):
    with brownie.reverts("dev: only owner"):
        swap.withdraw_admin_fees({'from': bob})
