import traceback
import SpotifyCredentials
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#authenticate without user, pull credentials from other file
credentials_manager = SpotifyClientCredentials(client_id=SpotifyCredentials.client_id,
client_secret=SpotifyCredentials.client_secret)

#sp = spotipy.Spotify(client_credentials_manager=credentials_manager)

playlistURL = "https://open.spotify.com/playlist/37i9dQZF1DXdQP3bGyOAvs?si=dce5cfef7a964b17"
playlist_URI = playlistURL.split("/")[-1].split("?")[0]

class SpotifyClass(spotipy.Spotify):
    def __init__(self,id):
        super().__init__(client_credentials_manager=id)

    def getPlaylistTracks(self,URL): 
        '''input Spotify URL, outputs a list of songs in (songName by songArtist)'''
        try:
            results = self.playlist_tracks(URL) #results
            tracks_result = results["items"] #filter to items
        except:
            print("ERROR: Couldn't find playlist")
            return -1
        while results["next"]: #results come in pages, go next
            results = self.next(results) #go to next page of results
            tracks_result.extend(results["items"]) #add the items to tracks_result

        songNameList = []
        for Track in tracks_result: #for each item in tracks_result: add songName and songArtist to output list
            try:
                songName = Track["track"]["name"]
                songArtist = Track["track"]["album"]["artists"][0]["name"]
                #print(songName,"by",songArtist)
                songNameList.append(songName+" by "+songArtist)
            except:
                print("ERROR: Couldn't find songName or songArtist")
        return songNameList
        

if __name__ == "__main__":
    sp1 = SpotifyClass(credentials_manager)
    #print(sp1.getPlaylistTracks(playlistURL))
    #print(len(sp1.getPlaylistTracks("https://open.spotify.com/playlist/2MavGhMNxUBbCP0CGOVFmg?si=96343331662b45c4")))
    print(sp1.getPlaylistTracks("wasd"))    