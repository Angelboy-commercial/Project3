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
from registerNFT import *

load_dotenv()

contract = load_contract()
r = Registration()

nft_data = {
    "NFT1" : r.nft_registration(self.tx_hash),
    "NFT2" : r.nft_registration(),
    "NFT3" : r.nft_registration()
}

nfts = ['NFT1', 'NFT2', 'NFT3']

def post_nft():
    list = list(nft_data.values())

    for number in range(len(nfts)):
        st.image
        st.write("name")
        st.write("description")
        st.write("min_bid")

st.title("Bid on NFTs Here!")

accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.write()

#Select NFT to bid on 
select_nft = st.selecbox('Choose NFT to bid on', nfts)

#Input starting bid
bid = st.number_input("Bid")

#Get art from dict
#Get art name
st.markdown("## NFT Name")
st.write(nft_data[nfts][])
#Artist name
st.markdown("## Artist Name")
st.write(nft_data[nfts][])
#Get description
st.markdown("## Description")
st.write(nft_data[nfts][])
#Get/write starting bid from dict
st.markdown("## Starting Bid")
st.write(nft_data[nfts][])



if st.button("Place Bid"):
    tx_hash = contract.functions.bid().transact({"from" : account, 'gas' : 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt)) 

if st.button("End"):
    tx_hash = contract.functions.auctioned()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))