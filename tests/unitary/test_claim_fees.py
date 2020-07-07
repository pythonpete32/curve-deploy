import brownie


def test_withdraw_only_owner(bob, swap):
    with brownie.reverts("dev: only owner"):
        swap.donate_admin_fees({'from': bob})


def test_donate_only_owner(bob, swap):
    with brownie.reverts("dev: only owner"):
        swap.withdraw_admin_fees({'from': bob})
