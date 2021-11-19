# Example code to call the SAP Conversational AI chat bot
import requests
import json 

token_url = 'oauth client url'

token_data = {
  'grant_type': 'client_credentials',
  'client_id': 'add your client id here',
  'client_secret': 'add your client secret here'
}

token_response = requests.post(token_url, data=token_data)
token_json_response = token_response.json()
bearer_token = token_json_response['access_token']
#print(token_json_response['access_token'])

bot_url = 'bot url'
bot_authorization = 'Bearer ' + bearer_token
#print(authorization + '\n') 

bot_headers = { 
        'Accept': 'application/json', 
        'Content-Type': 'application/json', 
        'Authorization': bot_authorization, 
        'X-Token': 'add your request token here'
}   

bot_data = '{"message": {"content":"add your message here","type":"text"}, "conversation_id":"add your id here"}'

# Call the SAP Conversational AI
response_chat = requests.post(bot_url, headers=bot_headers, data=bot_data) 
response_content = response_chat.content

results = json.loads(response_content)
#print(json.dumps(results, indent=2))

# Extract the response message from the chat bot
for messages in results["results"]["messages"]:
    print("\nMessage:", messages["content"])
