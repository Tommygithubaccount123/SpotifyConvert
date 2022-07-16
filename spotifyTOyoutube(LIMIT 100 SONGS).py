import SpotifyPlaylist, converter, SpotifyCredentials, concurrent.futures
from googleapiclient.discovery import build

api_key = SpotifyCredentials.youtube_api_key
api_name = "youtube"
api_version = "v3"
youtube_prefix_link = "https://www.youtube.com/watch?v="

def returnURL(name: str) -> str:
    '''input search term, returns first youtube link'''
    with build(api_name,api_version,developerKey=api_key) as ytService:
        searchList = ytService.search().list(part="id",q=str(name),maxResults=1,type="video")
        # print(searchList.execute()["items"][0]["id"]["videoId"])
    print("found youtube URL for",name)
    return youtube_prefix_link+searchList.execute()["items"][0]["id"]["videoId"]

def returnURL_List(spotifyPlaylistURL: str) -> list:
    output = []
    spotifyobj = SpotifyPlaylist.SpotifyClass(SpotifyPlaylist.credentials_manager)
    tracks = spotifyobj.getPlaylistTracks(spotifyPlaylistURL)
    if (len(tracks)<10):
        for i in tracks:
            output.append(returnURL(i))
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in tracks:
                output.append(executor.submit(returnURL,i).result())

    return output



if __name__ == "__main__":
    print(len(returnURL_List("https://open.spotify.com/playlist/2Xzh3AUllumMIUpoSP4pUg?si=3326b064ae624009")))