
N_COINS = 3  # DAI, USDC, USDT
PRECISIONS = [18, 6, 6]
USE_LENDING = [True, True, True]

replacements = {
    '___N_COINS___': str(N_COINS),
    '___PRECISION_MUL___': f"[{', '.join(str(10**18 // (10**i)) for i in PRECISIONS)}]",
    '___USE_LENDING___': f"[{', '.join(str(i) for i in USE_LENDING)}]"
}


def brownie_load_source(path, source):
    if path.stem in ("Deposit", "StableSwap"):
        for k, v in replacements.items():
            source = source.replace(k, v)

    return source
