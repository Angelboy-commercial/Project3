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

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

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

address = st.selectbox("Select Account:", options = accounts)
nft_id = st.selectbox("Select NFT:", options = [int(0)])
bid = st.text_input("Enter Bid:")

contract_address2 = os.getenv("SMART_CONTRACT_ADDRESS")
account = generate_account(w3)

if st.button("Place Bid"):
<<<<<<< HEAD
    #tx_hash = contract.functions.placeBid(nfts_options, int(bid)).transact({"to": contract_address2, "from" : '0x7223eA760A13D5DeCb09684C7276fE425A42eC80', 'gas' : 3000000, 'value': bid})
    #receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #ether = st.text_input("Input amount of ether")
    trans = send_transaction(w3, account, contract_address2, int(bid))
    st.write("Transaction receipt mined:")
    st.write(dict(trans))
    #st.write(dict(trans))
=======
    tx_hash = contract.functions.placeBid(nft_id, int(bid)).transact({"from" : address, 'gas' : 3000000, 'value': int(bid)})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
>>>>>>> 143529ffa8f9b908df3acb9537e2ad6c403de7c3

if st.button("Withdraw"):
    tx_hash = contract.functions.withdraw(1)
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

if st.button("View Token"):
    tx_hash = contract.functions.viewToken(1)
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
