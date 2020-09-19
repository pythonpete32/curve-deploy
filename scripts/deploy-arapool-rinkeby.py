# Testnet deployment script

import json
from web3 import middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy as gas_strategy
from brownie import (
        web3, accounts,
        ERC20CRV, VotingEscrow, ERC20, ERC20LP, CurvePool, Registry,
        GaugeController, Minter, LiquidityGauge, LiquidityGaugeReward, PoolProxy, CurveRewards
        )

SEED = 'explain tackle mirror kit van hammer degree position ginger unfair soup bonus'
confs = 1
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
ARAGON_AGENT = "0xa01556dB443292BD3754C1CCd0B9ecFE8CE9E356"
DISTRIBUTION_AMOUNT = 10 ** 6 * 10 ** 18
DISTRIBUTION_ADDRESSES = ["0xb4124cEB3451635DAcedd11767f004d8a28c6eE7", "0x8401Eb5ff34cc943f096A32EF3d5113FEbE8D4Eb"]

def main():
    accounts.from_mnemonic(SEED)
    admin = accounts[0]


    DaxToken = ERC20CRV.deploy("DAO JONES Token", "DAX", 18, {'from': admin, 'required_confs': confs})
    voting_escrow = VotingEscrow.deploy(
        DaxToken, "Vote-escrowed DAX", "veDAX", "veDAX_1.0.0", {'from': admin, 'required_confs': confs}
    )


    ant = ERC20.deploy("Aragon Network Token", "ANT", 18, {'from': admin, 'required_confs': confs})
    anj = ERC20.deploy("Aragon Network Juror", "ANJ", 18, {'from': admin, 'required_confs': confs})
    ant._mint_for_testing(10 ** 9 * 10 ** 18, {'from': admin, 'required_confs': confs})
    anj._mint_for_testing(10 ** 9 * 10 ** 18, {'from': admin, 'required_confs': confs})

    lp_token_AntPool = ERC20LP.deploy("ANT Pool", "antPool", 18, 0, {'from': admin, 'required_confs': confs})
    AntPool = CurvePool.deploy([ant, anj], lp_token_AntPool, 100, 4 * 10 ** 6, {'from': admin, 'required_confs': confs})
    lp_token_AntPool.set_minter(AntPool, {'from': admin, 'required_confs': confs})

    ant.approve(AntPool, "1000000000000000000000", {'from': admin})
    anj.approve(AntPool, "1000000000000000000000", {'from': admin})
    AntPool.add_liquidity(["100000000000000", "200000000000000"], 0, {'from': admin})

    # take a closer look at these contracts
    #DaoJonesRewards = CurveRewards.deploy(lp_token_AntPool, ant, {'from': accounts[0], 'required_confs': confs})
    #DaoJonesRewards.setRewardDistribution(accounts[0], {'from': accounts[0], 'required_confs': confs})
    registry = Registry.deploy([ZERO_ADDRESS] * 4, {'from': admin, 'required_confs': confs})

    #ant.transfer(DaoJonesRewards, 100e18, {'from': accounts[0], 'required_confs': confs})

    for account in DISTRIBUTION_ADDRESSES:
        ant.transfer(account, DISTRIBUTION_AMOUNT, {'from': admin, 'required_confs': confs})
        anj.transfer(account, DISTRIBUTION_AMOUNT, {'from': admin, 'required_confs': confs})

    AntPool.commit_transfer_ownership(ARAGON_AGENT, {'from': admin, 'required_confs': confs})
    AntPool.apply_transfer_ownership({'from': admin, 'required_confs': confs})
    registry.commit_transfer_ownership(ARAGON_AGENT, {'from': admin, 'required_confs': confs})
    registry.apply_transfer_ownership({'from': admin, 'required_confs': confs})

    gauge_controller = GaugeController.deploy(DaxToken, voting_escrow, {'from': admin, 'required_confs': confs})
    minter = Minter.deploy(DaxToken, gauge_controller, {'from': admin, 'required_confs': confs})
    liquidity_gauge = LiquidityGauge.deploy(lp_token_AntPool, minter, {'from': admin, 'required_confs': confs})

    DaxToken.set_minter(minter, {'from': admin, 'required_confs': confs})
    gauge_controller.add_type(b'Liquidity', {'from': admin, 'required_confs': confs})
    gauge_controller.change_type_weight(0, 10 ** 18, {'from': admin, 'required_confs': confs})
    gauge_controller.add_gauge(liquidity_gauge, 0, 10 ** 18, {'from': admin, 'required_confs': confs})

    gauge_controller.commit_transfer_ownership(ARAGON_AGENT, {'from': admin, 'required_confs': confs})
    gauge_controller.apply_transfer_ownership({'from': admin, 'required_confs': confs})
    voting_escrow.commit_transfer_ownership(ARAGON_AGENT, {'from': admin, 'required_confs': confs})
    voting_escrow.apply_transfer_ownership({'from': admin, 'required_confs': confs})


    PoolProxy.deploy({'from': admin, 'required_confs': confs})