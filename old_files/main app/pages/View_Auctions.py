from lib2to3.pgen2 import token
import os
import json
import requests
from unicodedata import name
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from bip44 import Wallet
from web3 import Account
from web3 import middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

pinata = Path("../../pinata.py")

#crypto_wallet = Path("../main app/crypto_wallet.py")
#contract = Path("../Project_3/contracts.py")
#from registerNFT import *

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

json_headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}


@st.cache(allow_output_mutation=True)
def load_contract(file):
    with open(Path(f"../contracts_json/{file}")) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("AUCTIONS_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

def convert_data_to_json(content):
    data = {"pinataOptions": {"cidVersion": 1}, "pinataContent": content}
    return json.dumps(data)

def pin_file_to_ipfs(data):
    r = requests.post("https://api.pinata.cloud/pinning/pinFileToIPFS", files = {'file': data}, headers = file_headers)
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_json_to_ipfs(json):
    r = requests.post("https://api.pinata.cloud/pinning/pinJSONToIPFS", data = json, headers = json_headers)
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_artwork(artwork_name, artwork_file):
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }

    json_data = convert_data_to_json(token_json)
    json_ipfs_hash = pin_json_to_ipfs(json_data)
    return json_ipfs_hash, token_json


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash

def generate_account(w3):
    mnemonic = os.getenv("MNEMONIC")
    wallet = Wallet(mnemonic)
    private, public = wallet.derive_account("eth")
    account = Account.privateKeyToAccount(private)
    return account

def send_transaction(w3, account, receiver, ether):
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
    wei_value = w3.toWei(ether, "ether")
    gas_estimate = w3.eth.estimateGas({"to": receiver, "from": account.address, "value": wei_value})

    raw_tx = {
        "to": receiver,
        "from": account.address,
        "value": wei_value,
        "gas": gas_estimate,
        "gasPrice": 0,
        "nonce": w3.eth.getTransactionCount(account.address)
    }

    signed_tx = account.signTransaction(raw_tx)
    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)

contract = load_contract("auctions.json")
accounts = w3.eth.accounts

contract_address2 = os.getenv("SMART_CONTRACT_ADDRESS")
account = generate_account(w3)

address = st.selectbox("Select Account:", options = accounts)
token_supply = contract.functions.totalSupply().call()

token_names = []
for i in range(0, token_supply):
    token_attributes = contract.functions.viewToken(int(i)).call()
    token_names.append((i, token_attributes[1]))

token_id = st.selectbox("Select Token:", options = token_names)

if st.button("View Token"):
    token_attributes = contract.functions.viewToken(int(token_id[0])).call()
    st.write(f"Token Creator: {token_attributes[0]}")
    st.write(f"Token Name: {token_attributes[1]}")
    st.write(f"Token Description: {token_attributes[2]}")
    st.write(f"Token Beneficiary: {token_attributes[3]}")

    if token_attributes[4] == True:
        st.write("Auction Complete")
    else:
        st.write("Auction Not Complete")

    st.write(f"Auction End Time: {token_attributes[5]}")
    st.write(f"Highest Bid: {token_attributes[6]}")
    st.write(f"Highest Bidder: {token_attributes[7]}")

bid = st.text_input("Enter Bid:")

if st.button("Place Bid"):
    bid = contract.functions.placeBid(token_id[0], int(bid)).transact({"from": address, 'gas': 3000000, 'value': int(bid)})
    receipt = w3.eth.waitForTransactionReceipt(bid)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

if st.button("View Current Bid"):
    current_bid = contract.functions.viewCurrentBalance(0).call()
    st.write(f"Current bid is {current_bid}")

if st.button("Withdraw"):
    withdraw = contract.functions.withdraw(int(token_id[0])).transact({"from": address, 'gas': 3000000})
    st.write("Bid withdrawn")
