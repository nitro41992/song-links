import requests
from json import dumps, loads
from flask import Flask, request
import os
import re

app = Flask(__name__)

links = {}
links['links'] = {}

yt_api_key = user_name = os.getenv('YT_MUSIC_KEY')
yt_music_search_val = '%20Auto-generated%20by%20YouTube.'
yt_base_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q="

spotify_client_id = user_name = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
spotify_token_url='https://accounts.spotify.com/api/token'



@app.route('/', methods=['GET'])
def home():
    return "<h1>Song Links</p>"

@app.route('/links/', methods=['POST'])
def get_links():
    if request.method == 'POST':
        response = request.json
        search = response['search']
        
        try:
            payload = {}
            headers = {'Accept': 'application/json'}
            yt_get_url = yt_base_url + search.replace(' ', '%20') + yt_music_search_val + '&videoLicense=any&key=' + yt_api_key
            response = requests.request("GET", yt_get_url, headers=headers, data = payload)
            response_json = response.json()
            video_id = response_json['items'][0]['id']['videoId']
        except:
            try:
                yt_get_url = 'https://www.youtube.com/results?search_query=' + search.replace(' ', '%20')
                pattern = re.compile(r'{"videoId":"([A-Za-z0-9]+)"')
                page = requests.request("GET", yt_get_url, headers={'Accept': 'application/json'}, data = {})
                video_id = re.findall(pattern, page.text)[0]
            except:
                yt_get_url = 'Could not find the song in Youtube Music.'

        yt_music_url = 'https://music.youtube.com/watch?v=' + video_id
        links['links']['YouTube Music'] = yt_music_url


        grant_type = 'client_credentials'
        body_params = {'grant_type' : grant_type}
        response = requests.post(spotify_token_url, data=body_params, auth = (spotify_client_id, spotify_client_secret)) 
        token_raw = loads(response.text)
        token = token_raw["access_token"]
        spotify_get_url = "https://api.spotify.com/v1/search?q=" + search.replace(' ', '%20') + "&type=track"
        payload = {}
        headers = {"Authorization": "Bearer {}".format(token)}
        try:
            response = requests.request("GET", spotify_get_url, headers=headers, data = payload)
            response_json = response.json()
            spotify_music_url = response_json['tracks']['items'][0]['external_urls']['spotify']
            links['Song Name'] = response_json['tracks']['items'][0]['name']
            links['Album Name'] = response_json['tracks']['items'][0]['album']['name']
            links['Artist Name'] = response_json['tracks']['items'][0]['artists'][0]['name']
        except:
            spotify_music_url = 'Could not find the song in Spotify Music.'
        links['links']['Spotify Music'] = spotify_music_url

        
        
        

        return(links)
        # return(response_json)

if __name__ == '__main__':
    app.run()