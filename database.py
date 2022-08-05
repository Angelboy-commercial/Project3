import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
# biding function
# crowdsale functionalities
# all methods being defined in auction.sol

conn = psycopg2.connect(
    host='localhost',
    dbname='suppliers',
    user='postgres',
    password='Theblockchainpapi34!',
    port=5432  
)
curse = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

insert_event = 'insert into NFTable(nft_id,nft_name,nft_uri,nft_file) values (%s,%s,%s,%s)'

def enter_event(nft_id,nft_name,nft_uri,nft_file):
    event_confirm = (nft_id,nft_name,nft_uri,nft_file)
    curse.execute(insert_event, event_confirm)
    conn.commit()
    curse.close()
    conn.close()

enter_event(1 , 'nfthoe', 'uri pa', 'song.mp3')

