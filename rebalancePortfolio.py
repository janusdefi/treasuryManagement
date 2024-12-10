from web3 import Web3




# Connect to Ethereum node
infura_url = "https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract and Wallet Details
treasury_address = "0xTreasuryContractAddress"
treasury_abi = [
    {
        "inputs": [],
        "name": "rebalancePortfolio",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]
private_key = "YOUR_PRIVATE_KEY"  # Replace with the private key of the wallet
wallet_address = "0xYourWalletAddress"

# Load Treasury Contract
treasury_contract = web3.eth.contract(address=treasury_address, abi=treasury_abi)

# Build and Sign Transaction
nonce = web3.eth.getTransactionCount(wallet_address)
gas_price = web3.eth.gas_price
transaction = treasury_contract.functions.rebalancePortfolio().buildTransaction({
    "chainId": 5,  # Goerli Testnet
    "gas": 500000,
    "gasPrice": gas_price,
    "nonce": nonce,
    "from": wallet_address,
})

signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(f"Transaction sent! Hash: {txn_hash.hex()}")

# Wait for Transaction Confirmation
receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Transaction confirmed! Block: {receipt.blockNumber}")
