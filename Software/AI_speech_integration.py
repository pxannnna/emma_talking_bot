"""
AI-Speech Integration code, that does:

    1- Speech to text conversion
    2- Generates AI model's response
    3- Converts Text to Speech

"""

# ------------------- Import Libraries -------------------
import vosk
import pyaudio
import json
import pygame
import google.generativeai as genai
import pyttsx3
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import *


# ------------------- Initializations -------------------

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize VOSK model
model = vosk.Model(VOSK_MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, VOSK_SAMPLE_RATE)

# Configure Gemini API with your API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize offline Text-to-Speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 170)
tts_engine.setProperty('volume', 1.0)

# Set voice to English (prefer female voice if available)
voices = tts_engine.getProperty('voices')
english_voices = [v for v in voices if 'en' in v.id.lower() or 'english' in v.name.lower()]
if english_voices:
    # Prefer female English voice, fallback to any English voice
    female_english = [v for v in english_voices if 'female' in v.name.lower() or 'woman' in v.name.lower()]
    if female_english:
        tts_engine.setProperty('voice', female_english[0].id)
        print(f"Using English female voice: {female_english[0].name}")
    else:
        tts_engine.setProperty('voice', english_voices[0].id)
        print(f"Using English voice: {english_voices[0].name}")
else:
    print("No English voices found, using default voice")



# ------------------- Utility Functions -------------------

def play_sound(file_path):
    """
    Plays an audio file using pygame.

    Args:
        file_path (str): Path to the audio file.
    """
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for audio to finish playing
        pygame.time.Clock().tick(5)

# ------------------- Speech-to-Text Function -------------------

def listen_with_vosk():
    """
    Captures audio from the microphone and converts it to text using VOSK.

    Returns:
        str: Transcribed text from speech.
    """
    mic = pyaudio.PyAudio()  # Initialize microphone
    stream = mic.open(
        format=pyaudio.paInt16, channels=AUDIO_CHANNELS, rate=VOSK_SAMPLE_RATE, input=True, frames_per_buffer=AUDIO_CHUNK_SIZE
    )
    stream.start_stream()
    print("Listening ...")
    play_sound(LISTEN_SOUND_PATH)  # Play listening sound

    while True:
        data = stream.read(AUDIO_CHUNK_SIZE)
        if len(data) == 0:  # Skip if no audio data
            continue

        if recognizer.AcceptWaveform(data):  # Recognize speech
            play_sound(CONVERT_SOUND_PATH)  # Play conversion sound
            result = recognizer.Result()  # Get result from recognizer
            text = json.loads(result)["text"]  # Extract text
            print("You said: " + text)
            return text

# ------------------- AI Text Generation Function -------------------

def gemini_api(text):
    """
    Sends input text to the Gemini API and retrieves the generated response.

    Args:
        text (str): Input text for the API.

    Returns:
        str: Generated response text from Gemini API.
    """
    # Initialize a genAI model
    model = genai.GenerativeModel(model_name=GEMINI_MODEL)

    # Generate a response based on the input text
    response = model.generate_content(text)
    print(response.text)  # Print the response
    return response.text

# ------------------- Text-to-Speech Function -------------------

def text_to_speech(text):
    """
    Converts input text to speech using offline pyttsx3 engine.

    Args:
        text (str): Text to convert to speech.
    """
    print(f"Emma says: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

# ------------------- Main Loop -------------------

# Continuously listen, process, and respond
while True:
    # Step 1: Convert speech to text
    text = listen_with_vosk()  # Speech recognition

    # Step 2: Generate a response using Gemini API
    ai_response = gemini_api(text)  # Text generation

    # Step 3: Convert the response to speech
    text_to_speech(ai_response)  # Text-to-speech
