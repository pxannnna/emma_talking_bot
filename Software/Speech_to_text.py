'''
1A - Speech to Text using Google's SpeechRecognition API
This script listens to the microphone, plays sound prompts,
and converts speech into text using Google's API.
'''

import speech_recognition as sr  # Library for speech-to-text
import pygame  # Library for playing audio files

# Initialize the pygame mixer for audio playback
pygame.mixer.init()

def play_sound(file_path):
    """
    Plays an audio file and waits until it finishes.
    :param file_path: Path to the audio file to play.
    """
    pygame.mixer.music.load(file_path)   # Load the sound file
    pygame.mixer.music.play()            # Start playing
    while pygame.mixer.music.get_busy(): # Wait until playback ends
        pygame.time.Clock().tick(5)      # Limit the loop speed

def listen_with_google():
    """
    Listens to the microphone, plays sound prompts,
    and returns recognized speech as text.
    """
    recognizer = sr.Recognizer()  # Create a speech recognizer

    with sr.Microphone() as source:  # Use the default microphone
        print("Listening ... ")
        play_sound("../Resources/listen.mp3")  # Play "listening" prompt

        audio = recognizer.listen(source)     # Capture speech from mic
        play_sound("../Resources/convert.mp3")# Play "processing" prompt

        # Optional: Adjust for background noise (commented out here)
        # recognizer.adjust_for_ambient_noise(source) # In case of noisy environment

        text = recognizer.recognize_google(audio)  # Convert speech to text
        print("You said: " + text)                 # Output recognized text
        return text

##-------- MAIN EXECUTION -----------

listen_with_google()  # Run the speech-to-text process
