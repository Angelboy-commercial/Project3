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
  
    
contract = load_contract("auctions.json")
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts


bid = st.number_input("Enter your bid")
nfts = "some dictionary of nfts"
address = st.selectbox("Select Account", options=accounts)

for nft in nfts:

    if st.button("View Token"):
        pass

    if st.button("Place Bid"):
        tx_hash = contract.functions.firstBid(address, int(bid)).transact({"from" : accounts, 'gas' : 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))

    if st.button("Withdraw"):
        tx_hash = contract.functions.withdraw()
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
    