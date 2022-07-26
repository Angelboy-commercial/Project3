from lib2to3.pgen2 import token
import os
import json
from unicodedata import name
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from pinata import *
from contracts import load_contract

load_dotenv()

#Load the contract
contract = load_contract()

def nft_registration():
    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
    st.title("Register NFT's Here")
    st.write("Select an account associated with the NFT")
    accounts = w3.eth.accounts
    address = st.selectbox("Select Account", options=accounts)
    st.markdown("---")

    st.markdown("## Registration")
    name = st.text_input("Enter the name of the artist")
    description = st.text_area("Enter a description of the NFT")
    starting_bid = st.text_input("Enter the starting bid")

    # Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
    file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png", "mp3"])

    if st.button("Register NFT"):
        ipfs_hash, token_json = pin_artwork(name, file)
        uri = f"ipfs://{ipfs_hash}"
        tx_hash = contract.functions.registerArtwork(
        address,
        name,
        description,
        int(starting_bid),
        uri,
        token_json['image']
    ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))



def post_nft():
    st.title("Auction For Charity")
    st.markdown("## Bid On An NFT!")
    st.text_input("Enter the artist name")
    st.text_area("Enter a description of the NFT")
    st.text_input("Starting")