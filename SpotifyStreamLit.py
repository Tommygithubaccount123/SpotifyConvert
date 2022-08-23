import streamlit as st
import tkinter as tk
from tkinter import filedialog
import SpotifyPlaylist
import os

cl_id = st.secrets["client_id"]
cl_secret = st.secrets["client_secret"]

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

class spotifyScript():
    def __init__(self):
        if ("folder_path" not in st.session_state): 
            st.session_state["folder_path"] = ""

        if ("spotify_url" not in st.session_state):
            st.session_state["spotify_url"] = ""
        self.folder_path = st.session_state["folder_path"]  #allows for not replace values after each rerun
        self.spotify_url = st.session_state["spotify_url"]

        st.title("Spotify Converter")
        st.markdown("1. Input Spotify playlist URL\n2. Select folder download path\n3. Press Download")

        text_input = st.text_input("Enter url")
        print("TEXT: "+text_input)
        st.session_state["spotify_url"] = text_input #take url
        self.spotify_url = text_input

        folder_button = st.button("Select Folder")
        download_button = st.button("Download")
        if folder_button:
            print("Folder pressed")

            self.folder_path = self.browseFolder()
            st.session_state["folder_path"] = self.folder_path
        if download_button:
            print("Download pressed")
            self.convert()

    def browseFolder(self):
        folder = tk.filedialog.askdirectory()
        st.markdown("Download path: " + folder) 
        print(folder)
        return folder

    def convert(self):
        print(f"PATH: {self.folder_path}, URL: {self.spotify_url}")
        if (self.spotify_url==""):
            st.markdown("ERROR: Enter url")
            print("ERROR: Enter url")
        elif (self.folder_path==""):
            st.markdown("ERROR: Select download path")
            print("ERROR: Select download path")
        else:
            print("Converting spotify playlist")
            try:
                failed_songs = SpotifyPlaylist.downloadTRACKS(self.spotify_url,self.folder_path)
                st.markdown("Finished downloading playlist")
                print("Finished downloading playlist")
            except:
                st.markdown("ERROR: URL did not work")
                print("ERROR: URL did not work")
                return -1
            if (len(failed_songs)==0):
                return 1
            else:
                failmessage = ""
                for i in range(len(failed_songs)):
                    failmessage += (f"{i}. ERROR: Failed to download {failed_songs[i]}\n")
                st.markdown(failmessage)
                print(failmessage)
                return -1

spotifyScript()