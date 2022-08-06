import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title = 'GiveCoin')
st.title('GiveCoin')

with st.container():
    left, right = st.columns(2)
    with left:
        st.write(''' We are a platform that simply put connects artists and art lovers. However, 
    all of these transactions are on the blockchain and for charity. Artists accounts can create
    NFTs that will be auctioned off to the charity of their choosing. These artists can range from 
    celebrities auctioning time with them or a singer uploading a song. 
    ''')

st.write('---')

with st.container():
    left, right = st.columns(2)
    with right:
        st.write('''They way it works is an artists chooses a charity of their choice. That 
    charity then provides an ethreum address that is entered in the contract as the beneficiary
    and everything from that point on works in a tradional auction way. Winning bidder claims the NFT
    (along with the mp3 file to download) and the proceeds get sent to the charity address.
    ''')
    
    # with right:
        # st.image('', width=300)
