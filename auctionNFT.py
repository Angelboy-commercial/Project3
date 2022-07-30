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
from crypto_wallet import *

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
# This is a test contract
contract = load_contract("ArtRegistrytest.json")
accounts = w3.eth.accounts
r = Registration(contract, w3, accounts)

# Retrieve a dictionary of the registered NFTS that will be displayed in the auction
def nft_data():
    nft_dict = {}
    # This locates the art collection in the contract where the outputs contain name, appraisal value, image of nft
    for dicts in contract[12]["outputs"]:
        for key, value in dicts.items():
            items = key, value
    return items.append(nft_dict)
# Desired outcome -> nft_dict = {'NFT1' : [Name, Artist, Address, Description, Starting bid, image uri],
#                            'NFT2' : [Name, Artist, Address, Description, Starting bid, image uri]
#                            'NFT3' : [Name, Artist, Address, Description, Starting bid, image uri] }

#Alternate version of nft_data to test and see which method works
#Will try incorporating registration function in this one function
#Could be the better option here
def nft_data2():
    r.nft_registration()
    nft_dict2 = {}
    for content in tx_hash:
        json_file = convert_data_to_json(content)
        for index in range(len(json_file)):
            try:
                address = json_file[index]['address']
                name = json_file[index]['name']
                artist = json_file[index]['artist']
                description = json_file[index]['description']
                starting_bid = json_file[index]['starting_bid']
                uri = json_file[index]['uri']

                nft_dict2['address'] = address
                nft_dict2['name'] = name
                nft_dict2['artist'] = artist
                nft_dict2['description'] = description
                nft_dict2['starting bid'] = starting_bid
                nft_dict2['image uri'] = uri

            except KeyError:
                print('na')
            
    return nft_dict2


# Retrieve keys of the nft_dict
def nfts():
    dict = nft_data()
    nfts = []
    for keys in dict:
        nft = keys
    return nft.append(nfts)
# Desired outcome -> nfts = ['NFT1', 'NFT2', 'NFT3']

nft_dict = nft_data()
nft_list = nfts()

# Displays nfts
def display_nft():
    list = list(nft_dict.values())

    for number in range(len(nft_list)):
        st.image(list[number[5]])
        st.write("name": list[number][0])
        st.write("artist" : list[number][1])
        st.write("address" : list[number][2])
        st.write("description" : list[number][3])
        st.write("min_bid" : list[number][4])


########
#Streamlit App
########

st.title("Bid on NFT's Here!!!")

display_nft()

#Select account to bid with
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
#Write customers account address down
st.write()

#Select NFT to bid on 
nft_list = st.selecbox('Choose NFT to bid on', nft_list)

#Input starting bid
bid = st.number_input("Bid")

#Need to identify nfts such as NFT1,NFT2, etc. 
nft_list = nft_dict[nft_list][0]

#Get art from dict
#Get art name
st.markdown("## NFT Name")
st.write(nft_list)
#Artist name
st.markdown("## Artist Name")
st.write(nft_dict[nft_list][1])
#Address
st.markdown("## Owner Address")
st.write(nft_dict[nft_list][2])
#Get description
st.markdown("## Description")
st.write(nft_dict[nft_list][3])
#Get/write starting bid from dict
st.markdown("## Starting Bid")
st.write(nft_dict[nft_list][4])



if st.button("Place Bid"):
    tx_hash = contract.functions.bid().transact({"from" : accounts, 'gas' : 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt)) 

if st.button("End"):
    tx_hash = contract.functions.auctioned()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

starting_bid = nft_dict[nft_list][4]
owner_address = nft_dict[nft_list][2]
if st.button("Send Transaction"):
    tx_hash = send_transaction(w3, accounts, owner_address, starting_bid)

    st.write("Transaction successful")
    st.write(tx_hash)