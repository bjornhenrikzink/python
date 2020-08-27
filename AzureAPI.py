import requests 
import json 
import time

#API1
try:
    rAPI = 'https://funcappdigitalcore.azurewebsites.net/api/HttpTriggerMyAPI2'
    rJson = requests.get(rAPI) 
    rJsonText = rJson.text

    rJsonLoad = json.loads(rJsonText) 

    print('\r' + 'API: ' + rAPI)
    print('\r' + 'JSON: ' + rJsonText)
    print('\r' + 'Name: ' + rJsonLoad['name'])
    print('\r' + 'Domain: ' + rJsonLoad['domain'])
    print('\r' + 'Product Area: ' + rJsonLoad['productarea'])
    print('\r' + 'Product Team: ' + rJsonLoad['productteam'])
except:
    print('did not work')

#API2
try:
    rAPI = 'https://funcappdigitalcore.azurewebsites.net/api/HttpTriggerMyAPI'
    rJson = requests.get(rAPI) 
    rJsonText = rJson.text

    rJsonLoad = json.loads(rJsonText) 

    print('\r' + 'API: ' + rAPI)
    print('\r' + 'JSON: ' + rJsonText)
    print('\r' + 'Name: ' + rJsonLoad['name'])
    print('\r' + 'Domain: ' + rJsonLoad['domain'])
    print('\r' + 'Product Area: ' + rJsonLoad['productarea'])
    print('\r' + 'Product Team: ' + rJsonLoad['productteam'])
except:
    print('did not work')