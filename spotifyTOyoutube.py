import SpotifyPlaylist, converter, SpotifyCredentials
from googleapiclient.discovery import build

key = SpotifyCredentials.youtube_api_key
api_name = "youtube"
api_version = "v3"

with build(api_name,api_version,key) as ytService:
    ytService.search()