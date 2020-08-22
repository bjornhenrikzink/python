import requests 
import json 
import time

from time import sleep

print('Azure:') 

rKeyValue = '4EJnQleetD64hIjxxuN9chPy9AYXcr2/5wjpV2F6ZMSDRCDvhruovQ=='
rRequestString = 'https://funcappdigitalcore.azurewebsites.net/api/HttpTriggerHelloWorldAPI?code=' + rKeyValue
print(rRequestString)
rString = requests.get(rRequestString)
rText = rString.text
print(rText)

"""

loops = 3

for i in range(loops):
    rString = requests.get('https://funcappdigitalcore.azurewebsites.net/api/HttpTriggerHelloWorldAPI')
    rText = rString.text
    print('/r' + rText),
    percent = ((i+1) / loops) * 100
    print('\r' + str(int(percent)) + '% completed'),
    time.sleep(10.0)

"""