
from web3 import Web3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
TREASURY_CONTRACT = os.getenv("TREASURY_CONTRACT")

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
assert web3.isConnected(), "Failed to connect to Ethereum node"

# Treasury Contract ABI (Simplified for this example)
TREASURY_ABI = [
    {
        "inputs": [],
        "name": "getActiveAssets",
        "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "rebalancePortfolio",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

# Load Treasury Contract
treasury_contract = web3.eth.contract(address=TREASURY_CONTRACT, abi=TREASURY_ABI)


# Fetch active assets
def get_active_assets():
    return treasury_contract.functions.getActiveAssets().call()


# Mock AI logic for rebalancing
def mock_ai_rebalance():
    active_assets = get_active_assets()
    print(f"Active Assets: {active_assets}")

    # Simulate rebalancing logic (assign equal weights for simplicity)
    new_allocations = [1000 for _ in active_assets]  # Mock allocations in token units
    return active_assets, new_allocations


# Submit rebalance transaction
def submit_rebalance(assets, allocations):
    # Build transaction
    nonce = web3.eth.getTransactionCount(WALLET_ADDRESS)
    gas_price = web3.eth.gas_price
    transaction = treasury_contract.functions.rebalancePortfolio().buildTransaction({
        "chainId": 5,  # Goerli Testnet
        "gas": 500000,
        "gasPrice": gas_price,
        "nonce": nonce,
        "from": WALLET_ADDRESS,
    })

    # Sign transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

    # Send transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction sent! Hash: {txn_hash.hex()}")

    # Wait for confirmation
    receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    print(f"Transaction confirmed! Block: {receipt.blockNumber}")


# Main function to run the AI agent
def main():
    print("Fetching active assets...")
    assets, allocations = mock_ai_rebalance()

    print(f"Proposed Allocations: {allocations}")
    print("Submitting rebalance transaction...")
    submit_rebalance(assets, allocations)


if __name__ == "__main__":
    main()
