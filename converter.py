from pytube import YouTube
from pytube import Playlist
import os, sys, datetime, concurrent.futures

def length(duration):
    return str(datetime.timedelta(seconds=duration))

def download_video(url, file_destination, type):
    '''input url and destination, downloads video
    download_video(url, file_destination, type 0=video 1=audio), returns -1 if error
    '''
    try:
        yt = YouTube(url)
    except:
        print("ERROR: Link did not work")
        return -1
    print("\nVideo found:",yt.title,"Length:", length(yt.length),"Views:",yt.views)
    
    #length check:
    if (yt.length/3600.0 > 1.0):
        print("TOO LONG:",yt.title,"Length",length(yt.length))
        return -1

    try:
        if (type == 0):
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.get_audio_only()
        print("\nVideo downloaded in", stream.download(output_path=file_destination))
        return 1
    except:
        print("FAILED to get stream")
        return -1

def menu():
    print("Options:")
    print("1. Video/Audio Download")
    print("2. Playlist Download")
    return input("Enter number: ")

def download_playlist(url, file_destination, type):
    '''input playlist url and destination, downloads playlist
        download_playlist(url, file_destination, type 0=video 1=audio)
    '''
    try:
        playlist = Playlist(url)
        play_list_duration = playlist.length
    except:
        print("ERROR: playlist url did not work")
        return -1
    print("\nPlaylist found:",playlist.title, play_list_duration,"videos")
    list_of_URL = playlist.video_urls
    if (play_list_duration < 5):
        for i in list_of_URL:
            download_video(i,file_destination,type)
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in list_of_URL:
                executor.submit(download_video,i,file_destination,type)
                

if __name__ == "__main__":
    start = menu()
    while (start != "1" and start !="2"):
        print()
        start = menu()
    
    requested_type = input("\nEnter 0 for video, 1 for audio ")
    while (requested_type != "0" and requested_type != "1"):
        requested_type = input("Enter 0 for video, 1 for audio: ")
    video_url = input("Enter URL: ")
    input_destination = input("Enter file destination (Press ENTER for downloads folder): ")
    if (input_destination == ""):
        input_destination = "C:\\Users\\stink\\Downloads"
    if (start == "1"):
        download_video(video_url, input_destination,int(requested_type))
    elif (start == "2"):
        download_playlist(video_url, input_destination, int(requested_type))