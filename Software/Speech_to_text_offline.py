'''
Step 1:
Speech to Text using VOSK offline API.
Unlike Google's API, VOSK works entirely offline after downloading a model.

Download VOSK model from: https://alphacephei.com/vosk/models
'''

import vosk      # Offline speech recognition library
import pyaudio   # Audio input from microphone
import json      # To parse recognition results
import pygame    # To play audio prompts

# Initialize pygame mixer for playing sounds
pygame.mixer.init()

# Load the VOSK speech recognition model
model = vosk.Model("../Resources/vosk-model-en-us-0.22")

# Create recognizer object for the model (sample rate 16000 Hz)
recognizer = vosk.KaldiRecognizer(model, 16000)

def play_sound(file_path):
    """
    Plays an audio file and waits until it finishes.
    :param file_path: Path to the audio file to play.
    """
    pygame.mixer.music.load(file_path)   # Load sound file
    pygame.mixer.music.play()            # Play sound
    while pygame.mixer.music.get_busy(): # Wait for playback to finish
        pygame.time.Clock().tick(5)      # Prevent high CPU usage

def listen_with_vosk():
    """
    Captures microphone input, recognizes speech offline using VOSK,
    and returns recognized text.
    """
    mic = pyaudio.PyAudio()  # Initialize audio input
    # Open audio stream from microphone
    stream = mic.open(
        format=pyaudio.paInt16,  # 16-bit audio
        channels=1,              # Mono audio
        rate=16000,               # Sample rate (Hz)
        input=True,               # Use as input (microphone)
        frames_per_buffer=8192    # Buffer size
    )
    stream.start_stream()

    print("Listening ...")
    play_sound("../Resources/listen.mp3")  # Play "listening" sound

    while True:
        data = stream.read(8192)  # Read audio from mic
        if len(data) == 0:        # Skip if no data
            continue

        # If a full phrase is recognized
        if recognizer.AcceptWaveform(data):
            play_sound("../Resources/convert.mp3")  # Play "processing" sound
            result = recognizer.Result()            # Get recognition result
            text = json.loads(result)["text"]       # Extract text from JSON
            print("You said: " + text)              # Display recognized text
            return text

###------------- MAIN LOOP -------------

while True:
    listen_with_vosk()  # Continuously listen and recognize speech
