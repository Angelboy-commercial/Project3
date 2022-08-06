import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title = 'GiveCoin')
st.title('GiveCoin')

with st.container():
    left, right = st.columns(2)
    with left:
        st.write("GiveCoin is a charitable giving platform allowing anyone to create decentralized, disintermediated charity auctions and crowdfunds on the Ethereum blockchin. Many different uses are possible. A celebrity could auction off a dinner with themself, the proceeds going to a charity address of their choice. GiveCoin could also function similarly to Make-A-Wish Foundation, where users would donate to a charity in support of a child's meeting their favorite author, or some other person they admire. GiveCoin can help connect artists and art lovers, to give another example. Artists could also create NFTs to be auctioned off, songs for example, with proceeds going to the charity of their choosing.")

st.write('---')

with st.container():
    left, right = st.columns(2)
    with right:
        st.write('''They way it works is an artist chooses a charity of their choice. That 
    charity then provides an ethereum address that is entered in the contract as the beneficiary,
    and everything from that point on works in a tradional auction way. The winning bidder claims the NFT
    along with the mp3 file to download, and the proceeds get sent to the charity address.
    ''')
    
    # with right:
        # st.image('', width=300)
