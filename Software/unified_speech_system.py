#!/usr/bin/env python3
"""
Unified Speech System for Emma Robot
Supports both online and offline speech recognition and text-to-speech
Configure via config.py to switch between modes
"""

import sys
import os
import json
import pygame
import pyaudio

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class UnifiedSpeechSystem:
    def __init__(self, use_offline_stt=True, use_offline_tts=False):
        """
        Initialize speech system
        
        Args:
            use_offline_stt (bool): Use VOSK (offline) vs Google (online) for speech-to-text
            use_offline_tts (bool): Use pyttsx3 (offline) vs OpenAI (online) for text-to-speech
        """
        self.use_offline_stt = use_offline_stt
        self.use_offline_tts = use_offline_tts
        
        # Initialize pygame for audio prompts
        pygame.mixer.init()
        
        # Initialize speech-to-text
        if use_offline_stt:
            self._init_vosk()
        else:
            self._init_google_stt()
            
        # Initialize text-to-speech
        if use_offline_tts:
            self._init_pyttsx3()
        else:
            self._init_openai_tts()
    
    def _init_vosk(self):
        """Initialize VOSK offline speech recognition"""
        import vosk
        self.vosk_model = vosk.Model(VOSK_MODEL_PATH)
        self.vosk_recognizer = vosk.KaldiRecognizer(self.vosk_model, VOSK_SAMPLE_RATE)
        print("✅ VOSK offline speech recognition initialized")
    
    def _init_google_stt(self):
        """Initialize Google online speech recognition"""
        import speech_recognition as sr
        self.google_recognizer = sr.Recognizer()
        print("✅ Google online speech recognition initialized")
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 offline text-to-speech"""
        import pyttsx3
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 170)
        self.tts_engine.setProperty('volume', 1.0)
        print("✅ pyttsx3 offline text-to-speech initialized")
    
    def _init_openai_tts(self):
        """Initialize OpenAI online text-to-speech"""
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI online text-to-speech initialized")
    
    def play_sound(self, file_path):
        """Play audio prompt"""
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(5)
    
    def listen(self):
        """Listen for speech and return text"""
        if self.use_offline_stt:
            return self._listen_vosk()
        else:
            return self._listen_google()
    
    def _listen_vosk(self):
        """Listen using VOSK (offline)"""
        mic = pyaudio.PyAudio()
        
        # Use smaller buffer to prevent overflow
        buffer_size = 4096  # Smaller than config
        
        stream = mic.open(
            format=pyaudio.paInt16,
            channels=AUDIO_CHANNELS,
            rate=VOSK_SAMPLE_RATE,
            input=True,
            frames_per_buffer=buffer_size,
            stream_callback=None
        )
        stream.start_stream()
        
        print("🎤 Listening (VOSK offline)...")
        print("💡 Speak clearly and wait for the 'convert' sound...")
        
        try:
            self.play_sound(LISTEN_SOUND_PATH)
        except:
            print("⚠️ Could not play listen sound, continuing...")
        
        while True:
            try:
                data = stream.read(buffer_size, exception_on_overflow=False)
                if len(data) == 0:
                    continue
                    
                if self.vosk_recognizer.AcceptWaveform(data):
                    try:
                        self.play_sound(CONVERT_SOUND_PATH)
                    except:
                        print("⚠️ Could not play convert sound, continuing...")
                    
                    result = self.vosk_recognizer.Result()
                    text = json.loads(result)["text"]
                    if text.strip():  # Only return non-empty text
                        print(f"🎯 You said: {text}")
                        stream.stop_stream()
                        stream.close()
                        mic.terminate()
                        return text
            except Exception as e:
                print(f"⚠️ Audio error: {e}")
                continue
    
    def _listen_google(self):
        """Listen using Google (online)"""
        import speech_recognition as sr
        
        with sr.Microphone() as source:
            print("🎤 Listening (Google online)...")
            self.play_sound(LISTEN_SOUND_PATH)
            
            audio = self.google_recognizer.listen(source)
            self.play_sound(CONVERT_SOUND_PATH)
            
            text = self.google_recognizer.recognize_google(audio)
            print(f"🎯 You said: {text}")
            return text
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"🗣️ Emma says: {text}")
        
        if self.use_offline_tts:
            self._speak_pyttsx3(text)
        else:
            self._speak_openai(text)
    
    def _speak_pyttsx3(self, text):
        """Speak using pyttsx3 (offline)"""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def _speak_openai(self, text):
        """Speak using OpenAI (online)"""
        import io
        
        response = self.openai_client.audio.speech.create(
            model=OPENAI_TTS_MODEL,
            voice=OPENAI_TTS_VOICE,
            input=text
        )
        
        audio_content = response.read()
        
        # Play audio using pygame
        pygame.mixer.music.load(io.BytesIO(audio_content))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

# Example usage
if __name__ == "__main__":
    # Configuration options:
    # 1. Fully offline (free, no internet needed)
    # speech_system = UnifiedSpeechSystem(use_offline_stt=True, use_offline_tts=True)
    
    # 2. Fully online (best quality, needs internet + costs money)
    # speech_system = UnifiedSpeechSystem(use_offline_stt=False, use_offline_tts=False)
    
    # 3. Hybrid (offline STT + online TTS - good balance)
    speech_system = UnifiedSpeechSystem(use_offline_stt=True, use_offline_tts=False)
    
    # Test the system
    print("🎯 Say 'quit' or 'exit' to stop the program")
    while True:
        text = speech_system.listen()
        
        # Check for exit commands
        if text.lower() in ['quit', 'exit', 'stop', 'goodbye']:
            speech_system.speak("Goodbye! See you later!")
            print("👋 Program stopped by user")
            break
            
        speech_system.speak(f"I heard you say: {text}")
