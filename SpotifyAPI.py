import requests 
import json 

# Get token from https://developer.spotify.com/console/get-artist/ and paste below
token = "" 
authorization = "'Bearer " + token + "'" 
print(authorization + '\n') 

headers = { 
    'Accept': 'application/json', 
    'Content-Type': 'application/json', 
    'Authorization': authorization, 
} 

# Artist 
req_artist = requests.get('https://api.spotify.com/v1/artists/4WwwNRj83Gcjv9L25kzGU0', headers=headers) 

req_artist_text = req_artist.text 
print('Artist text: \n' + req_artist_text + '\n') 

req_artist_json = req_artist.json() 
print('Artist JSON: \n' + str(req_artist_json) + '\n') 

req_artist_load = json.loads(req_artist_text) 
req_artist_name = req_artist_load["name"] 
print('Artist name: ' + str(req_artist_name) + '\n') 

# Get artists Top Track 
params = (('country', 'SE'),)    
req_top_tracks = requests.get('https://api.spotify.com/v1/artists/4WwwNRj83Gcjv9L25kzGU0/top-tracks', headers=headers, params=params) 
req_top_tracks_text = req_top_tracks.text 
req_top_tracks_load = json.loads(req_top_tracks_text) 

print(req_top_tracks_text + '\n') 

# List the artists top tracks
for i in req_top_tracks_load["tracks"]: 
    print('Artist top track #' + str(req_top_tracks_load["tracks"].index(i)+1) + f' {i["album"]["name"]}') 
