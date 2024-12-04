import requests
from bs4 import BeautifulSoup
from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("Connected to Ganache!")
else:
    print("Failed to connect to Ganache. Please check Ganache and URL.")
    exit()

web3.eth.default_account = web3.eth.accounts[0]

balance = web3.eth.get_balance(web3.eth.default_account)
print(f"Account Balance: {web3.from_wei(balance, 'ether')} ETH")

if balance == 0:
    print("Insufficient balance to perform transactions.")
    exit()

# ABI and contract address
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

contract_address = "0x73cd528f1AC73A2b629998e07900AAff8849009b"

scrape_storage = web3.eth.contract(address=contract_address, abi=contract_abi)


def extract_text_from_site(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None


# URL to scrape
url = "https://www.geeksforgeeks.org/"
site_text = extract_text_from_site(url)

if site_text:
    print(f"Scraped Data (preview): {site_text[:100]}...")

    try:
        tx_hash = scrape_storage.functions.storeData(site_text[:200]).transact(
            {"gas": 3000000}
        )
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print("Data stored in the blockchain.")
    except ValueError as e:
        print(f"Transaction failed: {e}")

    try:
        stored_data = scrape_storage.functions.retrieveData().call()
        print(f"Stored Data: {stored_data}")
    except ValueError as e:
        print(f"Error reading data from contract: {e}")
else:
    print("No data scraped from the website.")
