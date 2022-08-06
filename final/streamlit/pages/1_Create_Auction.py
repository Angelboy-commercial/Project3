from lib2to3.pgen2 import token
import os
import json
import requests
from unicodedata import name
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
pinata = Path('../pinata.py')
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URI')))

file_headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'), 'pinata_secret_api_key': os.getenv('PINATA_SECRET_API_KEY')}
json_headers = {'Content-Type': 'application/json', 'pinata_api_key': os.getenv('PINATA_API_KEY'), 'pinata_secret_api_key': os.getenv('PINATA_SECRET_API_KEY')}

@st.cache(allow_output_mutation = True)
def load_contract(file):
    with open(Path(f'../json_files/{file}')) as f:
        abi = json.load(f)
    contract_address = os.getenv('AUCTIONS_CONTRACT_ADDRESS')
    contract = w3.eth.contract(address = contract_address, abi = abi)
    return contract

def convert_data_to_json(content):
    data = {'pinataOptions': {'cidVersion': 1}, 'pinataContent': content}
    return json.dumps(data)

def pin_file_to_ipfs(data):
    r = requests.post('https://api.pinata.cloud/pinning/pinFileToIPFS', files = {'file': data}, headers = file_headers)
    print(r.json())
    ipfs_hash = r.json()['IpfsHash']
    return ipfs_hash

def pin_json_to_ipfs(json):
    r = requests.post('https://api.pinata.cloud/pinning/pinJSONToIPFS', data = json, headers = json_headers)
    print(r.json())
    ipfs_hash = r.json()['IpfsHash']
    return ipfs_hash

def pin_artwork(artwork_name, artwork_file):
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())
    token_json = {'name': artwork_name, 'image': ipfs_file_hash}
    json_data = convert_data_to_json(token_json)
    json_ipfs_hash = pin_json_to_ipfs(json_data)
    return json_ipfs_hash, token_json

def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash

accounts = w3.eth.accounts
contract = load_contract('auctions.json')

st.title('Create Auction')

creator_address = st.selectbox('Creator Address', options = accounts)
auction_name = st.text_input('Name')
description = st.text_area('Description')
beneficiary_address = st.text_input('Benficiary Address')
starting_bid = st.text_input('Starting Bid')
end_time = st.text_input('Auction End Time')

file = st.file_uploader('Attached Media', type = ['jpg', 'jpeg', 'png', 'mp3', 'mp4'])

if st.button('Submit'):
    ipfs_hash, token_json = pin_artwork(auction_name, file)
    uri = f'ipfs://{ipfs_hash}'
    print(auction_name, description, starting_bid, uri)
    
    submission = contract.functions.createToken(auction_name, description, beneficiary_address, int(end_time), uri).transact({'from': creator_address, 'gas': 1000000})
    receipt = w3.eth.getTransactionReceipt(submission)
    st.image(f"https://ipfs.io/ipfs/{token_json['image']}")
    st.markdown(f'[Attached Media Link](https://ipfs.io/ipfs/{ipfs_hash})')
    st.write('Transaction Receipt')
    st.write(dict(receipt))
