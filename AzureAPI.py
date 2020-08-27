import requests 
import json 
import time

def exceptionHandling(api):
    print('\r' + 'Oops, it did not work!' + '\r')
    print('\r' + api + '\r')

#API1
try:
    print('\r')
    print('\r' + 'Gitpod calling!' + '\r')
    print('\r')

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
    exceptionHandling(rAPI)

#API2
try:
    print('\r')
    print('\r' + 'Gitpod calling!' + '\r')
    print('\r')

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
    exceptionHandling(rAPI)

