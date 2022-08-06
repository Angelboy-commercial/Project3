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
    contract_address = os.getenv('CROWDFUNDING_CONTRACT_ADDRESS')
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
contract = load_contract('crowdfunds.json')

st.title("View Crowdfunds")
sender_address = st.selectbox("Sender Address", options = accounts)

with st.container():
    left, right = st.columns(2)

    with left:
        token_supply = contract.functions.totalSupply().call()

        token_names = []
        for i in range(0, token_supply):
            token_attributes = contract.functions.viewToken(int(i)).call()
            token_names.append((i, token_attributes[1]))

        token_id = st.selectbox('Crowdfunds', options = token_names)

        if st.button('View Crowdfund'):
            st.write(f"Sender's Contribution: {contract.functions.viewSenderContribution(token_id[0]).call({'from': sender_address})}")
            token_attributes = contract.functions.viewToken(int(token_id[0])).call()
            st.write(f'Creator: {token_attributes[0]}')
            st.write(f'Name: {token_attributes[1]}')
            st.write(f'Description: {token_attributes[2]}')
            st.write(f'Beneficiary: {token_attributes[3]}')

            if token_attributes[4] == True:
                st.write('Crowdfund Complete')
            else:
                st.write('Crowdfund Not Complete')

            st.write(f'Total Donations: {token_attributes[5]}')
            st.write(f'Biggest Donor: {token_attributes[6]}')

        if st.button('View Sender Contributions'):
            token_names = []
            for i in range(0, token_supply):
                if contract.functions.viewSenderContribution(i).call({'from': sender_address}) > 0:
                    token_attributes = contract.functions.viewToken(int(i)).call()
                    st.write(f"{i}/{token_attributes[1]}: {contract.functions.viewSenderContribution(int(i)).call({'from': sender_address})}")

    with right:
            donation = st.text_input('New Donation')

            if st.button('Make Donation'):
                donation = contract.functions.donate(token_id[0]).transact({'from': sender_address, 'gas': 3000000, 'value': int(donation)})
                receipt = w3.eth.waitForTransactionReceipt(donation)
                st.write('Transaction receipt mined:')
                st.write(dict(receipt))

            if st.button('Claim End'):
                end = contract.functions.end(int(token_id[0])).transact({'from': sender_address, 'gas': 3000000})
                st.write('Crowdfund Ended')
                
st.write('---')
