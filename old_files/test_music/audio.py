from audioop import add
import sounddevice
from scipy.io.wavfile import write
import streamlit as st 
from tkinter import *
import pygame
import json
import psycopg2
import psycopg2.extras
import pandas as pd



conn = psycopg2.connect(
    host='localhost',
    dbname='suppliers',
    user='postgres',
    password=,
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


# creating functions to interact with the NFT is cool ways such as 
# being able to attach a .wav to an NFT wiht the auctioner explaing the prize
# For music NFT attaching the audio to the song to the NFT to play while being aucitoned

# creating the functions sometimes without neccessary arguments as these arguemnts
# are created in the main file this will be imported to

# create voice recording for auctioner
def create_recording(file_length, filename):
    filename = filename.replace(" ","")
    fps = 44100
    file = sounddevice.rec(int(file_length*fps), samplerate=fps, channels=2)
    sounddevice.wait()
    print("Recording over")
    write(f"{filename}.wav", fps,file)

file_length = st.number_input('File length( 1.00 = 1 second)')
file_name = st.text_input('File name')
uri = st.text_input('uri')
# creating code to be copy and pasted into main file
if st.button('Record'):
    recorded = create_recording(file_length, file_name)


# How can I factor in transfering the mp3 to the winning bidder to download
# How do I connent the song to the NFT?
# The same thing for Event details through recoring 
# create a dictionary from transaction hash to mp3 file?
# create a function that allows for an auction winner to download the mp3


mp3_to_TxHash = {"Uri":[], "File":[]}

st.cache(allow_output_mutation=True)
def add_nft(file,uri):
    mp3_to_TxHash['Uri'].append(uri)
    mp3_to_TxHash['File'].append(file)
    return mp3_to_TxHash

def retreive_file(uri, nft_dictionary):
    file = nft_dictionary[uri]
    return file

def play_mp3(song):
    st.audio(song)

def show_image(Nft_id):
    st.image(Nft_id)

def play_mp4(uri, nft_dictionary):
    st.video(retreive_file(uri, nft_dictionary))

def download_file(uri, nft_dictionary):
    download = retreive_file(uri, nft_dictionary)
    st.download_button(download)

def return_dictionary():
    return mp3_to_TxHash

def song_query(id):
        query = f'''select * from NFTable where nft_id = {id}'''
        nft_db = pd.read_sql_query(query, con = conn)
        song = nft_db['nft_file'].to_list()
        play_mp3(song[0])

def image_query(id):
    query = f'''select * from NFTable where nft_id = {id}'''
    nft_db = pd.read_sql_query(query, con = conn)
    image = nft_db['nft_file'].to_list()
    show_image(image[0])




nft_id = st.text_input('Song id')
if st.button('View mp3 Nft'):
    song_query(nft_id)
    

if st.button('View Image Nft'):
    image_query(nft_id)




