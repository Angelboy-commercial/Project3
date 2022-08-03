from audioop import add
import sounddevice
from scipy.io.wavfile import write
import streamlit as st 
from tkinter import *
import pygame
import json

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


mp3_to_TxHash = {}


def add_nft(file,uri, nft_dictionary):
    nft_dictionary[uri] = file
    return nft_dictionary

def retreive_file(uri, nft_dictionary):
    file = nft_dictionary[uri]
    return file

def play_mp3(uri, nft_dictionary):
    st.audio(retreive_file(uri, nft_dictionary))

def show_image(uri,nft_dictionary):
    st.image(retreive_file(uri, nft_dictionary))

def play_mp4(uri, nft_dictionary):
    st.video(retreive_file(uri, nft_dictionary))

def download_file(uri, nft_dictionary):
    download = retreive_file(uri, nft_dictionary)
    st.download_button(download)

def return_dictionary():
    return mp3_to_TxHash



if st.button('play mp3'):
    mp3_to_TxHash = add_nft(file_name, uri, mp3_to_TxHash)
    play_mp3(uri, mp3_to_TxHash)
    st.write(return_dictionary())


# fileType = st.selectbox('File type', ['image','mp3', 'mp4'])






