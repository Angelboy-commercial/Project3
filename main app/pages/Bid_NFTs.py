from lib2to3.pgen2 import token
import os
import json
import requests
from unicodedata import name
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

#contract = Path("../Project_3/contracts.py")
pinata = Path("../Project_3/pinata.py")
#from registerNFT import *

load_dotenv()
  
# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

@st.cache(allow_output_mutation=True)
def load_contract(file):

    # Load the contract ABI
    with open(Path(f"../contracts_json/{file}")) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

    
file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

json_headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

def convert_data_to_json(content):
    data = {"pinataOptions": {"cidVersion": 1}, "pinataContent": content}
    return json.dumps(data)

def pin_file_to_ipfs(data):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        files={'file': data},
        headers=file_headers
    )
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_json_to_ipfs(json):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        data=json,
        headers=json_headers
    )
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash

contract = load_contract("auctions.json")
#w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts

nft_database = {
    "NFT1": ["Kodak Black", "description", "0xf36A6D75C6aFcb463303c12C12EF0Bb243eeF1b2", 16374829124, 3, "https://gateway.pinata.cloud/ipfs/QmT3zaTzsojQC4UuNGCDWgxs4vbcpu5PzYCDdvbVaxauc4/NFT1.png"],
    "NFT2": ["Kendall Jenner", "description", "0xf36A6D75C6aFcb463303c12C12EF0Bb243eeF1b2", 16374829124, 3, "https://gateway.pinata.cloud/ipfs/QmX2dXq79pzsuWAyi8gbaPYTW18J3CMz8z9SP1EmcpscNd/NFT2.png"]}

nfts = ['NFT1', 'NFT2']

address = st.selectbox("Select Account", options=accounts)
nfts_options = st.selectbox("Select NFTS", options=[0])
bid = st.text_input("Enter your bid")

# def get_nft(number):
#     nft_list = list(nft_database.values())

#     for number in range(len(nfts)):
#         st.image(nft_list[number][5])
#         st.write("Name: ", nft_list[number][0])
#         st.write("Description: ", nft_list[number][1])
#         st.write("Ethereum Account Address: ", nft_list[number][2])
#         st.write("Auction End Time: ", nft_list[number][3])
#         st.write("Starting Bid: ", nft_list[number][4], "ETH")
#         st.text(" \n")

# for value in (range(len(nfts_options))):

#     get_nft(value)

if st.button("Place Bid"):
    tx_hash = contract.functions.placeBid(nfts_options, int(bid)).transact({"from" : address, 'gas' : 3000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

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

    