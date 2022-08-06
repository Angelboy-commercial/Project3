import streamlit as st
# What I need to get done before meeting
# 1) create the Homepage 
# 2) prepare for other files to be intergrated on their respective pages
# 3) Create a  multipage app


# Step 1 CREATE THE HOMEPAGE IN THIS FILE
st.set_page_config(page_title='NFTea', page_icon=':cocktail:',layout='wide')


st.title('Brainstem')

st.subheader('We connect vital things.')

with st.container():
    left, right = st.columns(2)
    with left:
        st.write(''' We are a platform that simply put connects artists and art lovers. However, 
    all of these transactions are on the blockchain and for charity. Artists accounts can create
    NFTs that will be auctioned off to the charity of their choosing. These artists can range from 
    celebrities auctioning time with them or a singer uploading a song. 
    ''')

    with left:
        st.write('''They way it works is an artists chooses a charity of their choice. That 
    charity then provides an ethreum address that is entered in the contract as the beneficiary
    and everything from that point on works in a tradional auction way. Winning bidder claims the NFT
    (along with the mp3 file to download) and the proceeds get sent to the charity address.
    ''')
    
    with right:
        st.image('../images/brainstem.jpeg', width=300)
       
    

# idea on each page we can have a video of each of us  explaing the funcitonality of the page 