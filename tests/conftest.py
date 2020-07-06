import pytest

N_COINS = 3
PRECISIONS = [18, 6, 6]


# isolation setup

@pytest.fixture(autouse=True)
def isolation_setup(fn_isolation):
    pass


# named accounts

@pytest.fixture(scope="session")
def alice(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def bob(accounts):
    yield accounts[1]


@pytest.fixture(scope="session")
def charlie(accounts):
    yield accounts[2]


# contract deployments

@pytest.fixture(scope="module")
def underlying_coins(ERC20Mock, alice):
    coins = []

    for i in range(N_COINS):
        coin = ERC20Mock.deploy(
            f"Coin {i}", f"C{i}", PRECISIONS[i], {'from': alice}
        )
        coins.append(coin)

    yield coins


@pytest.fixture(scope="module")
def pool_token(CurveToken, alice):
    yield CurveToken.deploy(f"Stableswap", "STBL", 18, 0, {'from': alice})


@pytest.fixture(scope="module")
def aave_coins(ATokenMock, alice):
    coins = []
    for i in range(N_COINS):
        coin = ATokenMock.deploy(f"ACoin {i}", f"A{i}", PRECISIONS[i], {'from': alice})
        coins.append(coin)

    yield coins


@pytest.fixture(scope="module")
def swap(StableSwap, alice, underlying_coins, aave_coins, pool_token):
    contract = StableSwap.deploy(
        aave_coins, underlying_coins, pool_token, pool_token, 360 * 2, 10**7, {'from': alice}
    )
    pool_token.set_minter(contract, {'from': alice})

    yield contract


def approx(a, b, precision=1e-10):
    return 2 * abs(a - b) / (a + b) <= precision


@pytest.fixture(scope='function')
def deposit(Deposit, alice, coins, cerc20s, pool_token, swap):
    yield Deposit.deploy(cerc20s, coins, swap, pool_token, {'from': alice})
