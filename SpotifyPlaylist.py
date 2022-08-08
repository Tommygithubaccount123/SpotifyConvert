import SpotifyCredentials, spotipy, concurrent.futures, converter
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch

#authenticate without user, pull credentials from other file
credentials_manager = SpotifyClientCredentials(client_id=SpotifyCredentials.client_id,
client_secret=SpotifyCredentials.client_secret)

#playlistURL = "https://open.spotify.com/playlist/37i9dQZF1DXdQP3bGyOAvs?si=dce5cfef7a964b17"
#playlist_URI = playlistURL.split("/")[-1].split("?")[0]

class SpotifyClass(spotipy.Spotify):
    def __init__(self,id):
        super().__init__(client_credentials_manager=id)

    def getPlaylistTracks(self,URL: str) -> list: 
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
                songNameList.append(songName+" by "+songArtist+" audio")
            except:
                print("ERROR: Couldn't find songName or songArtist")
        return songNameList
        
def convertsongsURL(url: str) -> tuple:
    '''input spotify playlist url, returns tuple of (list of youtube urls, list of failed tracks)'''
    output = []
    failed_links = []
    SpotObj = SpotifyClass(credentials_manager)
    tracks = SpotObj.getPlaylistTracks(url)
    x = 1
    for i in tracks:
        try:
            videoResults = VideosSearch(i,limit=1)
            output.append(videoResults.result()["result"][0]["link"])
            print(f"{x}. Found Youtube link for", i)
        except:
            failed_links.append(i)
            print(f"{x}. Did not find link for", i)
        x += 1
    return (output,failed_links)

def downloadTRACKS(spotifyURL: str,folder_path: str) -> list:
    '''input spotify playlist URL and folder_path, downloads tracks, returns failed songs'''
    (valid_tracks, failed_tracks) =  convertsongsURL(spotifyURL)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in valid_tracks:
            # if (executor.submit(converter.download_video,i,folder_path,1).result()==-1): #KEEP COMMENTED, DOES NOT ALLOW PARALLEL TASKS
            #     failed_tracks.append(i) 
            executor.submit(converter.download_video,i,folder_path,1)
    return failed_tracks
if __name__ == "__main__": 
    downloadTRACKS("https://open.spotify.com/playlist/1bEut5XwCWU0IRMy8Wp6OH?si=6cf2f14fa7bf460a")