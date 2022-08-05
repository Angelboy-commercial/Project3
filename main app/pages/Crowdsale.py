from lib2to3.pgen2 import token
import os
import json
import requests
from unicodedata import name
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

<<<<<<< HEAD


=======
>>>>>>> 36b0c500bedc97c442477f62eacbb2f4e4d4db99
#contract = Path("../Project_3/contracts.py")
pinata = Path("../Project_3/pinata.py")
#from registerNFT import *

<<<<<<< HEAD
audio = Path("../Project_3/test_music/audio.py")
=======
>>>>>>> 36b0c500bedc97c442477f62eacbb2f4e4d4db99
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

<<<<<<< HEAD
    
=======
>>>>>>> 36b0c500bedc97c442477f62eacbb2f4e4d4db99
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
<<<<<<< HEAD
# w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts

st.title("Register Crowdfund here")
=======
#w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts

st.title("Crowdfund here")
>>>>>>> 36b0c500bedc97c442477f62eacbb2f4e4d4db99
st.write("Select an account associated with the NFT")

address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

st.markdown("## Registration")
<<<<<<< HEAD
name_ = st.text_input("Enter the name of the NFT")
description = st.text_area("Enter a description of the NFT")
starting_bid = st.text_input("Enter the starting bid")
#bool


end_time = st.number_input("Auction End Time")



=======
name_ = st.text_input("Enter the name")
description = st.text_area("Enter a description")
>>>>>>> 36b0c500bedc97c442477f62eacbb2f4e4d4db99

# Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png", "mp3", "mp4"])

<<<<<<< HEAD
if st.button("Register Crowdfund NFT"):
    ipfs_hash, token_json = pin_artwork(name_, file)
    uri = f"ipfs://{ipfs_hash}"
    print(name_, description, starting_bid, uri)
=======
if st.button("Register Crowdfund"):
    ipfs_hash, token_json = pin_artwork(name_, file)
    uri = f"ipfs://{ipfs_hash}"
    print(name_, description, address, uri)
>>>>>>> 36b0c500bedc97c442477f62eacbb2f4e4d4db99
    tx_hash = contract.functions.createToken(
        name_,
        description,
        address,
        uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.getTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
<<<<<<< HEAD



st.write("---")

if st.button("Donate here"):
    token_id = st.text_input('Enter the Token Id here')
    ipfs_hash, token_json = pin_artwork(name_, file)
    uri = f"ipfs://{ipfs_hash}"
    print(name_, description, starting_bid, uri)
    tx_hash = contract.functions.donate(
        token_id 
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.getTransactionReceipt(tx_hash)



if st.button('View Top Donors'):
    pass



st.write("---")



    
if st.button('View Crowdsale Nfts here'):
    token_type = st.selectbox('File type', ['mp3', 'image'])
    token_id = st.text_input('Enter the Token Id here')
    if token_type == 'mp3':

        audio.song_query(token_id)
    else:
        audio.image_query(token_id)


=======
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{ipfs_hash})")
    st.markdown(f"[Artwork IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")

if st.button("End"):
    pass

if st.button("Donate"):
    pass

if st.button("View Token"):
    pass
>>>>>>> 36b0c500bedc97c442477f62eacbb2f4e4d4db99
