import brownie

MIN_RAMP_TIME = 86400


def test_ramp_A(rpc, alice, swap):
    initial_A = swap.initial_A()
    future_time = rpc.time() + MIN_RAMP_TIME+5

    tx = swap.ramp_A(initial_A * 2, future_time, {'from': alice})

    assert swap.initial_A() == initial_A
    assert swap.future_A() == initial_A * 2
    assert swap.initial_A_time() == tx.timestamp
    assert swap.future_A_time() == future_time


def test_ramp_A_final(rpc, alice, swap):
    initial_A = swap.initial_A()
    future_time = rpc.time() + 1000000

    swap.ramp_A(initial_A * 2, future_time, {'from': alice})

    rpc.sleep(1000000)
    rpc.mine()

    assert swap.A() == initial_A * 2


def test_ramp_A_value_up(rpc, alice, swap):
    initial_A = swap.initial_A()
    future_time = rpc.time() + 1000000
    tx = swap.ramp_A(initial_A * 2, future_time, {'from': alice})

    initial_time = tx.timestamp
    duration = future_time - tx.timestamp

    while rpc.time() < future_time:
        rpc.sleep(100000)
        rpc.mine()
        expected = int(initial_A + ((rpc.time()-initial_time) / duration) * initial_A)
        assert 0.999 < expected / swap.A() <= 1


def test_ramp_A_value_down(rpc, alice, swap):
    initial_A = swap.initial_A()
    future_time = rpc.time() + 1000000
    tx = swap.ramp_A(0, future_time, {'from': alice})

    initial_time = tx.timestamp
    duration = future_time - tx.timestamp

    while rpc.time() < future_time:
        rpc.sleep(100000)
        rpc.mine()
        expected = int(initial_A - ((rpc.time()-initial_time) / duration) * initial_A)
        if expected == 0:
            assert swap.A() == 0
        else:
            assert 0.999 < swap.A() / expected <= 1


def test_stop_ramp_A(rpc, alice, swap):
    initial_A = swap.initial_A()
    future_time = rpc.time() + 1000000
    swap.ramp_A(initial_A * 2, future_time, {'from': alice})

    rpc.sleep(31337)

    current_A = swap.A.transact({'from': alice}).return_value

    swap.stop_ramp_A({'from': alice})

    assert swap.initial_A() == current_A
    assert swap.future_A() == current_A
    assert swap.initial_A_time() == 0
    assert swap.future_A_time() == 0


def test_ramp_A_only_owner(rpc, bob, swap):
    with brownie.reverts("dev: only owner"):
        swap.ramp_A(0, rpc.time()+1000000, {'from': bob})


def test_ramp_A_insufficient_time(rpc, alice, swap):
    with brownie.reverts("dev: insufficient time"):
        swap.ramp_A(0, rpc.time()+MIN_RAMP_TIME-1, {'from': alice})


def test_stop_ramp_A_only_owner(rpc, bob, swap):
    with brownie.reverts("dev: only owner"):
        swap.stop_ramp_A({'from': bob})
