import shutil
from scripts.helpful_scripts import get_account, get_contract
from brownie import Kell_Token, TokenFarm, network, config, web3
import yaml
import json
import os
import shutil

KEPT_BALANCE = web3.toWei(100, "ether")

def deploy_token_farm_and_kell_token(front_end_update=False):
    account = get_account()
    kell_token = Kell_Token.deploy({"from": account})
    token_farm = TokenFarm.deploy(kell_token.address, {"from": account}, publish_source=config["networks"][network.show_active()].get("verify,false"))
    tx = kell_token.transfer(token_farm.address, kell_token.totalSupply() - KEPT_BALANCE, {"from": account})
    tx.wait(1)
    kell_token = get_contract("kell_token")
    weth_token = get_contract("weth_token")
    fau_token = get_contract ("fau_token")
    dict_of_allowed_tokens = {
        kell_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("eth_usd_price_feed"),
    }
    
    # kell_token, weth_token, fau_token(faucet token "DAI")
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    if front_end_update:
        update_front_end() 
    return token_farm, kell_token

def add_allowed_tokens(tokens_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = tokens_farm.addAllowedTokens(token.address,{"from": account})
        add_tx.wait(1)
        set_tx = tokens_farm.setPriceFeedContract(token.address, dict_of_allowed_tokens[token],{"from": account})
        set_tx.wait(1)
        return tokens_farm

def update_front_end():
    # Sending the build folder to the front end 
    copy_folder_to_front_end("./build", "./front_end/src/chain-info")

    
    # Tyscript does not work with yaml files , so we'll need to convert our brownie-config to json file 
    # and Send to the front end config in json format
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", "w") as brownied_config_json:
            json.dump(config_dict,brownied_config_json)
            print("Front end updated!")


# Copy our build folder to our front_end
def copy_folder_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src,dest)

def main():
    deploy_token_farm_and_kell_token(front_end_update=True)