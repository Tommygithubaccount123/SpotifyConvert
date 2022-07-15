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
        self.TrackNames = self.playlist_tracks(URL)["items"]
        songNameList = []
        for Track in self.TrackNames:
            songName = Track["track"]["name"]
            songArtist = Track["track"]["album"]["artists"][0]["name"]
            #print(songName,"by",songArtist)
            songNameList.append(songName+" by "+songArtist)
        return songNameList
        

if __name__ == "__main__":
    sp1 = SpotifyClass(credentials_manager)
    print(sp1.getPlaylistTracks(playlistURL))