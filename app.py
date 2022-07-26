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

pages = {
    "Register NFT": nft_registration,
    "Test 1": test
}

nav_pages = st.sidebar.selectbox("Choose Page", pages.keys())
pages[nav_pages]()
