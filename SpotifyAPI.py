import requests 
import json 

token = "BQB4vja1wrSEoVvNktcxMxZGzlvSEJ52B4yjBDGmShsGdoPEkdJH-U2ff-GzVaOUlIHqjFJLOOQFmUrZV8dEi0PX4sljfDTGi80B177FixsEZsPrsbOHCJ8qXY5KfNQBttxY8K5wmQF2DlQdhFmJ-XnAXCGKLu_FvkEWPclKykZUA7-WgeSzpCHVxTRVTtMEK710wMBosTJ8SGvkB9bxIlBQCAXurUenwjmXClYPOhVURhPNrw1ZN9EPCmMfUBmCN9vcnd4LaIxHdBW7HSAaKl8" 
authorization = "'Bearer " + token + "'" 

#print('')
print(authorization) 
#print('') 
#print('Halloj') 
<<<<<<< HEAD
#print('Halloj again') 
=======
>>>>>>> 8f4a05dd93e17d96b65aa2642615608cd2ee3c0a

headers = { 
    'Accept': 'application/json', 
    'Content-Type': 'application/json', 
    'Authorization': authorization, 
} 

rArtist = requests.get('https://api.spotify.com/v1/artists/4WwwNRj83Gcjv9L25kzGU0', headers=headers) 

rArtistText = rArtist.text 

print('Text:') 
print(rArtistText) 
print(' ') 

rArtistJson = rArtist.json() 
print('Json:') 
print(rArtistJson) 
print(' ') 

rArtistLoad = json.loads(rArtistText) 
rArtistName = rArtistLoad["name"] 

print('Artist name: ' + rArtistName) 

# 
# Get Artists Top Track 
# 

params = ( 
    ('country', 'SE'), 
) 

rTopTracks = requests.get('https://api.spotify.com/v1/artists/4WwwNRj83Gcjv9L25kzGU0/top-tracks', headers=headers, params=params) 
rTopTracksText = rTopTracks.text 
rTopTracksLoad = json.loads(rTopTracksText) 

print('') 
print(rTopTracksText) 
print('') 

cnt = 1 

for i in rTopTracksLoad["tracks"]: 
    print('Top track #' + str(cnt) + f' {i["album"]["name"]}') 
    cnt += 1 
