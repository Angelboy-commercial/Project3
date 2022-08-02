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

def test():
    st.markdown("Bid")

contract = load_contract("nft.json")
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts

r = Registration(contract, w3, accounts)
#r.view_balance()
#r.view_balance()

pages = {
    "Register NFT": r.nft_registration(),
    "Auction": "add function",
    "Test 1": test()
}

#nav_pages = st.sidebar.selectbox("Choose Page", pages.keys())
#pages[nav_pages]()
