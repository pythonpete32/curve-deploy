import pytest

N_COINS = 3
PRECISIONS = [18, 6, 6]
TETHERED = [False, True, False]

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
def underlying_coins(ERC20Mock, ERC20MockReturnNone, alice):
    coins = []

    for i in range(N_COINS):
        deployer = ERC20MockReturnNone if TETHERED[i] else ERC20Mock
        coin = deployer.deploy(f"Coin {i}", f"C{i}", PRECISIONS[i], {'from': alice})
        coins.append(coin)

    yield coins


@pytest.fixture(scope="module")
def pool_token(CurveToken, alice):
    yield CurveToken.deploy(f"Stableswap", "STBL", 18, 0, {'from': alice})


@pytest.fixture(scope="module")
def aave_coins(ATokenMock, alice, underlying_coins, aave_lending_pool):
    coins = []
    for i, coin in enumerate(underlying_coins):
        coin_address = aave_lending_pool.deployToken(f"ACoin {i}", f"A{i}", coin).return_value
        coins.append(ATokenMock.at(coin_address))

    yield coins


@pytest.fixture(scope="module")
def aave_lending_pool(AaveLendingPoolMock, alice):
    yield AaveLendingPoolMock.deploy({'from': alice})


@pytest.fixture(scope="module")
def swap(StableSwap, alice, underlying_coins, aave_coins, pool_token, aave_lending_pool):
    contract = StableSwap.deploy(
        aave_coins, underlying_coins, pool_token, aave_lending_pool, 360 * 2, 0, {'from': alice}
    )
    pool_token.set_minter(contract, {'from': alice})

    yield contract


def approx(a, b, precision=1e-10):
    return 2 * abs(a - b) / (a + b) <= precision


@pytest.fixture(scope='function')
def deposit(Deposit, alice, coins, cerc20s, pool_token, swap):
    yield Deposit.deploy(cerc20s, coins, swap, pool_token, {'from': alice})
