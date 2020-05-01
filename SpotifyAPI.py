import requests 
import json 

token = "BQBqeF65Osc7fO1XTDpuZ3_EioaxqqI1PMcZSFGFIs6YD3w-uZJSb7wcQD3PzbVlzuTND_dNYqjeNnoZFw0D66k_o0KJi7l8iLasYzESP2-Gphk8dztV4L_bHiCRHt-qd2UryqHWunX_w_AA0GQT746jadq2JW8VeoJvKKQvaP8_0-pdaKVui9lBAJhHmUuIlGmZCJxhxoZXxPmazj9xcvofFmhQivbrT3bwVEkUBnWl3NYKev_hEoeJ6-wGDUzCdECqr_AUvkxDpEKWu8klzx4" 
authorization = "'Bearer " + token + "'" 

#print('')
#print(authorization) 
#print('') 

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
