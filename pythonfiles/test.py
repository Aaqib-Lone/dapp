from web3 import Web3

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    print("Failed to connect to Ganache.")
    exit()

web3.eth.default_account = web3.eth.accounts[0]
contract_address = "0xed3F79fdc550cc4000E96bf6D003208A369f99aF"

# ABI
contract_abi = [
    {
        "constant": False,
        "inputs": [{"name": "_data", "type": "string"}],
        "name": "storeData",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "retrieveData",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

# Instantiate the contract
scrape_storage = web3.eth.contract(address=contract_address, abi=contract_abi)

# Test the contract
try:
    # Store data
    print("Storing data...")
    tx_hash = scrape_storage.functions.storeData("Hello, Blockchain!").transact(
        {"from": web3.eth.default_account, "gas": 5000000}
    )
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Data stored successfully!")

    # Retrieve data
    print("Retrieving data...")
    result = scrape_storage.functions.retrieveData().call()
    print(f"Retrieved data: {result}")
except Exception as e:
    print(f"Error interacting with the contract: {e}")
