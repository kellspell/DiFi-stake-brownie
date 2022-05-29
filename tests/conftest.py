from scripts.helpful_scripts import get_account
import pytest
from web3 import Web3
from scripts.helpful_scripts import get_account
from brownie import MockKELL


@pytest.fixture
def amount_staked():
    return Web3.toWei(1, "ether")

@pytest.fixture
def random_erc20():
    account = get_account()
    erc20 = MockKELL.deploy({"from": account})
    return erc20