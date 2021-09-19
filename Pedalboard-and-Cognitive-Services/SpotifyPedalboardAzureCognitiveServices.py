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
    LowpassFilter,
    Distortion,
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
            #Compressor(threshold_db=-25, ratio=10),
            #Limiter(),
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
    # Initialize command
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


def execute_command(command, board, audio_file, sample_rate):
    # It would probably be more elegant to use a
    # language understanding app, such as LUIS, recognizing
    # the commands 

    # Speech recognition variations of "play the bass"
    command_play_bass = [
            'play the bass.',
            'play bass.', 
            'play the bass line.',
            'play bass line.',
            ]

    # Speech recognition variations of "play the bass with pedalboard"
    command_play_bass_with_pedalboard = [
            'play the bass with pedal board.',
            'play the bass with paddle boat.', 
            'play the bass with paddle board.',
            'play the bass wood pedalboard.',
            'play bass with pedal board.',
            'play bass with paddle boat.', 
            'play bass with paddle board.',
            'play bass wood pedalboard.',
            ]

    # Speech recognition variations of "add phaser"
    command_add_phaser = [
            'add face a.',
            'add facer.', 
            'add paper',    
            'at face a.'         
            ]

    # Speech recognition variations of "remove phaser"
    command_remove_phaser = [
            'remove face a.',
            'remove facer.',     
            ]        

    # Speech recognition variations of "add lowpass filter"
    command_add_lowpass_filter = [
            'at low pass filter.',
            'add low pass filter.', 
            ]

    # Speech recognition variations of "remove lowpass filter"
    command_remove_lowpass_filter = [
            'remove low pass filter.',
            ]  

    # Speech recognition variations of "add distortion"
    command_add_distortion = [
            'at distortion.',
            'add distortion.', 
            ]

    # Speech recognition variations of "remove distortion"
    command_remove_distortion = [
            'remove distortion.',
            ]              

    # Initialize response
    response = ''

    if command in command_play_bass:
        playsound('Bass.wav')
    elif command in command_play_bass_with_pedalboard:
        playsound_with_pedalboard(board, audio_file, sample_rate)
    elif command=='add chorus.':
        board.append(Chorus())
        response = 'chorus added to pedal board'
    elif command=='remove chorus.':
        remove_plugin(board, 'Chorus')
        response = 'chorus removed from pedal board'    
    elif command in command_add_phaser:
        board.append(Phaser())
        response = 'phaser added to pedal board'
    elif command in command_remove_phaser:
        remove_plugin(board, 'Phaser')
        response = 'phaser removed from pedal board'    
    elif command=='add reverb.':
        board.append(Reverb())
        response = 'reverb added to pedal board'
    elif command=='remove reverb.':
        remove_plugin(board, 'Reverb')
        response = 'reverb removed from pedal board'        
    elif command in command_add_lowpass_filter:
        board.append(LowpassFilter(cutoff_frequency_hz = 5000))
        response = 'Lowpass Filter added to pedal board'
    elif command in command_remove_lowpass_filter:
        remove_plugin(board, 'LowpassFilter')
        response = 'Lowpass Filter removed from pedal board'   
    elif command in command_add_distortion:
        board.append(Distortion())
        response = 'Distortion added to pedal board'
    elif command in command_remove_distortion:
        remove_plugin(board, 'LowpassFilter')
        response = 'Distortion removed from pedal board'   
             
    # Write out the pedelboard effects to verify correct command execution
    print("Pedalboard effect:\n")
    print('\n'.join(map(str, board))) 

    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = 'en-GB-Susan' # add this
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