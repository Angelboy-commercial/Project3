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
contract = load_contract("ArtRegistrytest.json")
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


class Registration:
    accounts = w3.eth.accounts

    def nft_registration(self):
    
        st.title("Register NFT's Here")
        st.write("Select an account associated with the NFT")

        address = st.selectbox("Select Account", options=self.accounts, key=0)
        st.markdown("---")

        st.markdown("## Registration")
        name = st.text_input("Enter the name of the artist")
        description = st.text_area("Enter a description of the NFT")
        starting_bid = st.number_input("Enter the starting bid")

        # Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
        file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png", "mp3"])

        if st.button("Register NFT"):
            ipfs_hash, token_json = pin_artwork(name, file)
            uri = f"ipfs://{ipfs_hash}"
            print(name, description, starting_bid, uri)
            self.tx_hash = contract.functions.registerNFT(
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
            st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
            st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{ipfs_hash})")

    def view_balance(self):
        st.markdown("## Check Balance of an Account")

        selected_address = st.selectbox("Select Account", options=self.accounts, key=1)

        tokens = contract.functions.balanceOf(selected_address).call()

        st.write(f"This address owns {tokens} tokens")

        st.markdown("## Check  Ownership and Display Token")

        total_token_supply = contract.functions.totalSupply().call()

        token_id = st.selectbox("Artwork Tokens", list(range(total_token_supply)))

        if st.button("Display"):

            # Get the art token owner
            owner = contract.functions.ownerOf(token_id).call()

            st.write(f"The token is registered to {owner}")

            # Get the art token's URI
            token_uri = contract.functions.tokenURI(token_id).call()

            st.write(f"The tokenURI is {token_uri}")
            st.image(token_uri)

    



def post_nft():
    st.title("Auction For Charity")
    st.markdown("## Bid On An NFT!")
    st.text_input("Enter the artist name")
    st.text_area("Enter a description of the NFT")
    st.text_input("Starting")