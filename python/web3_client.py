from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy


MY_KEY = "REPLACE_THIS"
MY_ADDRESS = "REPLACE_THIS"
CONTRACT_ADDRESS = "REPLACE_THIS"
SETUP_ADDRESS = "REPLACE_THIS"

# generated with `solc --abi Setup.sol`
SETUP_ABI = """
REPLACE_THIS
"""

# generated with `solc --abi Contract.sol`
CONTRACT_ABI = """
REPLACE_THIS
"""

#--------------------------------------------------------------------#
#                          Connection info                           #
#--------------------------------------------------------------------#
w3: Web3 = Web3(Web3.HTTPProvider("http://REPLACE_THIS/rpc"))
w3.eth.set_gas_price_strategy(medium_gas_price_strategy)
nonce = w3.eth.get_transaction_count(MY_ADDRESS)  # type: ignore

my_contract = w3.eth.contract(address=SETUP_ADDRESS, abi=SETUP_ABI)  # type: ignore
print("is connected:", w3.is_connected(), w3.eth.chain_id)

print("is solved:", my_contract.functions.isSolved().call())

# Remove to execute below code
exit(0)


my_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)  # type: ignore
print("is connected:", w3.is_connected(), w3.eth.chain_id)

def strong_attack(damage):
    #--------------------------------------------------------------------#
    #                   Gas estimate based on function                   #
    #--------------------------------------------------------------------#
    gas_estimate = my_contract.functions.strongAttack(damage).estimate_gas() * 2
    print("gas_estimate", gas_estimate)

    #--------------------------------------------------------------------#
    #                      Transaction With Params                       #
    #--------------------------------------------------------------------#
    punch_txn = my_contract.functions.strongAttack(damage).build_transaction(
        {
            "chainId": w3.eth.chain_id,
            "gas": gas_estimate,
            "gasPrice": w3.eth.generate_gas_price(),
            "nonce": nonce,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(punch_txn, MY_KEY)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    return txn_receipt

def punch():
    #--------------------------------------------------------------------#
    #                   Gas estimate based on function                   #
    #--------------------------------------------------------------------#
    gas_estimate = my_contract.functions.punch().estimate_gas()
    print("gas_estimate", gas_estimate)

    #--------------------------------------------------------------------#
    #                        Transaction Building                        #
    #--------------------------------------------------------------------#
    punch_txn = my_contract.functions.punch().build_transaction(
        {
            "chainId": w3.eth.chain_id,
            "gas": gas_estimate,
            "gasPrice": w3.eth.generate_gas_price(),
            "nonce": nonce,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(punch_txn, MY_KEY)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    return txn_receipt

def loot():
    #--------------------------------------------------------------------#
    #                   Gas estimate based on function                   #
    #--------------------------------------------------------------------#
    gas_estimate = my_contract.functions.loot().estimate_gas()
    print("gas_estimate", gas_estimate)
    #--------------------------------------------------------------------#
    #                        Transaction Building                        #
    #--------------------------------------------------------------------#
    loot_txn = my_contract.functions.loot().build_transaction(
        {
            "chainId": w3.eth.chain_id,
            "gas": gas_estimate,
            "gasPrice": w3.eth.generate_gas_price(),
            "nonce": nonce,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(loot_txn, MY_KEY)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    return txn_receipt


def my_balance():
    wei_balance = w3.eth.get_balance(MY_ADDRESS) # type: ignore
    eth_balance = w3.from_wei(wei_balance, "ether")

    print("wei_balance", wei_balance)
    print("eth_balance", eth_balance)

print("Life Points:", my_contract.functions.lifePoints().call())
my_balance()
# print("Receipt: ", strong_attack(20))
# print("Receipt: ", punch())
print("Receipt: ", loot())
print("Life Points:", my_contract.functions.lifePoints().call())

