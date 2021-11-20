from dotenv import load_dotenv
from playsound import playsound
from pedalboard import (
    Pedalboard,
    Convolution,
    Compressor,
    Distortion,
    Chorus,
    Gain,
    Reverb,
    Limiter,
    Phaser,
)
import os
import requests
import json

# Import namespaces
import soundfile as sf
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config

        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('AZURE_COG_SERVICE_KEY')
        cog_region = os.getenv('AZURE_COG_SERVICE_REGION')

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
        print('\n\nWelcome to the Spotify Pedalboard DAW using Azure Cognitive Services and SAP Conversational AI!\n')

        # Get raw audio file and sample rate
        audio_file, sample_rate = sf.read('Bass.wav')
    
        # Make a Pedalboard object, containing multiple plugins:
        board = Pedalboard([
        #    Compressor(threshold_db=-25, ratio=10),
        #    Gain(gain_db=10),
        #    Limiter(),
        ], sample_rate=sample_rate)

        # Get Token Bearer for SAP Conversational AI Music Studio Bot
        token_url = os.getenv('SAP_CAI_TOKEN_URL')
        token_client_id = os.getenv('SAP_CAI_ClIENT_ID')
        token_client_secret = os.getenv('SAP_CAI_CLIENT_SECRET')
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': token_client_id,
            'client_secret': token_client_secret
        }
        token_response = requests.post(token_url, data=token_data)
        token_response_json = token_response.json()
        token = token_response_json['access_token']
        
        bot_url = os.getenv('SAP_CAI_MUSIC_STUDIO_BOT_URL')
        bot_authorization = 'Bearer ' + token
        bot_x_token = os.getenv('SAP_CAI_X_TOKEN')
        bot_headers = { 
            'Accept': 'application/json', 
            'Content-Type': 'application/json', 
            'Authorization': bot_authorization, 
            'X-Token': bot_x_token
        }   

        # This is where the action is!
        # Get user input
        command = ''
        while command != 'quit session.':
            azure_speech_to_text_command = transcribe_command().lower()

            # Use SAP CAI to figure out intent
            sap_cai_intent = chat_command(azure_speech_to_text_command, bot_url, bot_headers)

            # Execute command based on intent
            execute_command(sap_cai_intent, board, audio_file, sample_rate)

            if sap_cai_intent == 'quit session.' or sap_cai_intent == 'Bye bye':
                command = 'quit session.'

    except Exception as ex:
        print(ex)

# Call Azure Speech to text recognition
def transcribe_command():
    command = ''

    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('\nSpeak now...')

    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print("Azure Cognitive Services: " + command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)
    
    # Return the command
    return command

# Call SAP Conversational AI with Music Studio Bot to figure out command
def chat_command(command, bot_url, bot_headers):

    # JSON message to send to the the Music Studio Bot
    bot_data =  '{"message": {"content":"' + command + '","type":"text"}, "conversation_id":"123"}'
    print("Chat message send to SAP CAI: " + command)
    bot_chat = requests.post(bot_url, headers=bot_headers, data=bot_data) 
    bot_content = bot_chat.content
    bot_results = json.loads(bot_content)
    #print(json.dumps(bot_results, indent=2))

    # Extract the detected language name for each document
    for bot_messages in bot_results["results"]["messages"]:
        command = bot_messages["content"]
        print("Chat response from SAP CAI:", bot_messages["content"])

    return command

def execute_command(question, board, audio_file, sample_rate):
    response = ''

    if question=='Play the bass':
        playsound('Bass.wav')
    elif question=='Play the bass with pedal board':
        playsound_with_pedalboard(board, audio_file, sample_rate)
    elif question=='Add distortion':
        board.append(Distortion())
        response = 'distortion added to pedal board'
        print_effects(board)
    elif question=='Remove distortion':
        remove_plugin(board, 'Distortion')
        response = 'distortion removed from pedal board'
        print_effects(board)
    elif question=='Add chorus':
        board.append(Chorus())
        response = 'chorus added to pedal board'
        print_effects(board)
    elif question=='Remove chorus':
        remove_plugin(board, 'Chorus')
        response = 'chorus removed from pedal board'    
        print_effects(board)
    elif question=='Add phaser':
        board.append(Phaser())
        response = 'phaser added to pedal board'
        print_effects(board)
    elif question=='Remove phaser':
        remove_plugin(board, 'Phaser')
        response = 'phaser removed from pedal board'    
        print_effects(board)
    elif question=='Add reverb':
        board.append(Reverb())
        response = 'teverb added to pedal board'
        print_effects(board)
    elif question=='Remove reverb':
        remove_plugin(board, 'Reverb')
        response = 'reverb removed from pedal board'    
        print_effects(board)
    else:
        response = question        

    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = 'en-GB-RyanNeural' 
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)   

    if response!='':
        # Synthesize spoken output
        speak = speech_synthesizer.speak_text_async(response).get()
        if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
            print(speak.reason)

def print_effects(board):
    # Write out the effects of the pedelboard to verify command execution
    print("\nEffects of the Pedalboard:")
    print('\n'.join(map(str, board))) 

def remove_plugin(board, plugin_str):
    for plugin in board:
        if type(plugin).__name__ == plugin_str:
            board.remove(plugin)

def playsound_with_pedalboard(board, audio_file, sample_rate):
    # Run the audio through this pedalboard!
    audio_with_effects = board(audio_file)
    audio_file_with_effects = 'BassWithEffects.wav'

    # Write the audio back as a wav file:
    with sf.SoundFile(audio_file_with_effects, 'w', samplerate=sample_rate, channels=len(audio_with_effects.shape)) as f:
        f.write(audio_with_effects)

    # Play audio with pedalboard effects
    playsound(audio_file_with_effects)   

if __name__ == "__main__":
    main()
