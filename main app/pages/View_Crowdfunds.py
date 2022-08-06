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

audio = Path("../Project_3/test_music/audio.py")
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

contract = load_contract("crowdfunding.json")
# w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts

st.title("Register Crowdfund here")
st.write("Select an account associated with the NFT")

address = st.selectbox("Select Account", options=accounts)
st.markdown("---")


token_id = st.text_input("Token Id")




st.write("---")


donation = st.text_input("Donation Amount")

if st.button("Donate"):
    tx_hash = contract.functions.donate(int(token_id)).transact({"from" : address, 'gas' : 3000000, 'value': int(donation)})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))




st.write("---")


if st.button("End Auction"):
    tx_hash = tx_hash = contract.functions.end(int(token_id)).transact({"from" : address, 'gas' : 3000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))