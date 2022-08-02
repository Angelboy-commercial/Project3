from lib2to3.pgen2 import token
import os
import json
from unicodedata import name
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from pinata import *
from registerNFT import *

load_dotenv()

contract = load_contract("nft.json")
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts

st.title("Register NFT's Here")
st.write("Select an account associated with the NFT")

address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

st.markdown("## Registration")
name_ = st.text_input("Enter the name of the NFT")
description = st.text_area("Enter a description of the NFT")
starting_bid = st.text_input("Enter the starting bid")
#bool
auction_complete = st.checkbox("Auction Completed")
if auction_complete:
    st.write("Auction Completed")

end_time = st.number_input("Auction End Time")
min_bid = st.number_input("Minimum bid")
highest_bid = st.number_input("Highest bid")

# Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png", "mp3", "mp4"])

if st.button("Register NFT"):
    ipfs_hash, token_json = pin_artwork(name_, file)
    uri = f"ipfs://{ipfs_hash}"
    print(name_, description, starting_bid, uri)
    tx_hash = contract.functions.createToken(

    )