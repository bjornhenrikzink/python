from dotenv import load_dotenv
from playsound import playsound
from pedalboard import (
    Pedalboard,
    Convolution,
    Compressor,
    Chorus,
    Gain,
    Reverb,
    Limiter,
    Phaser,
)
import os
import soundfile as sf

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config

        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
        print('Ready to use Pedalboard DAW:', speech_config.region)

        # Get raw audio file and sample rate
        audio_file, sample_rate = sf.read('Bass.wav')
    
        # Make a Pedalboard object, containing multiple plugins:
        board = Pedalboard([
            Compressor(threshold_db=-25, ratio=10),
            Gain(gain_db=10),
            Limiter(),
        ], sample_rate=sample_rate)

        # Get user input
        command = ''
        while command != 'quit session.':
            command = transcribe_command().lower()

            if command != 'quit session.':
                execute_command(command, board, audio_file, sample_rate)
            else:
                command = 'quit session.'

    except Exception as ex:
        print(ex)

def transcribe_command():
    command = ''

    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now...')

    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command

def execute_command(question, board, audio_file, sample_rate):
    response = ''

    if question=='play the bass.':
        playsound('Bass.wav')
    elif question=='play the bass with pedal board.' or question=='play the bass with paddle boat.' or question=='play the bass with paddle board.' or question=='play the bass wood pedalboard.' :
        playsound_with_pedalboard(board, audio_file, sample_rate)
    elif question=='add chorus.':
        board.append(Chorus())
        response = 'chorus added to pedal board'
    elif question=='remove chorus.':
        remove_plugin(board, 'Chorus')
        response = 'chorus removed from pedal board'    
    elif question=='add face a.' or question=='add facer.' or question=='add paper' or question=='at face a.':
        board.append(Phaser())
        response = 'phaser added to pedal board'
    elif question=='remove face a.' or question=='remove facer.':
        remove_plugin(board, 'Phaser')
        response = 'phaser removed from pedal board'    
    elif question=='add reverb.':
        board.append(Reverb())
        response = 'reverb added to pedal board'
    elif question=='remove reverb.':
        remove_plugin(board, 'Reverb')
        response = 'reverb removed from pedal board'        

    # Write out the effects of the pedelboard to verify command execution
    print("Effects of the Pedalboard:\n")
    print('\n'.join(map(str, board))) 

    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = 'en-GB-George' # add this
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)   

    if response!='':
        # Synthesize spoken output
        speak = speech_synthesizer.speak_text_async(response).get()
        if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
            print(speak.reason)

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