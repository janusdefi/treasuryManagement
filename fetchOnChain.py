from web3 import Web3

# Connect to Ethereum node
infura_url = "https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Treasury Contract Details
treasury_address = "0xTreasuryContractAddress"
treasury_abi = [
    {
        "inputs": [],
        "name": "getActiveAssets",
        "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# Load Treasury Contract
treasury_contract = web3.eth.contract(address=treasury_address, abi=treasury_abi)

# Fetch active assets
active_assets = treasury_contract.functions.getActiveAssets().call()
print("Active Assets in Treasury:", active_assets)
