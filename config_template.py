# Configuration template for Emma Robot Project
# Copy this file to config.py and add your API keys

import os

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
GEMINI_MODEL = "gemini-1.5-flash-latest"

# OpenAI Text-to-Speech Configuration (ChatGPT Quality)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
OPENAI_TTS_MODEL = "tts-1"                   # OpenAI TTS model
OPENAI_TTS_VOICE = "nova"                    # Voice options: alloy, echo, fable, onyx, nova, shimmer

# VOSK Speech Recognition Configuration
VOSK_MODEL_PATH = "Resources/vosk-model-en-us-0.22"
VOSK_SAMPLE_RATE = 16000

# Audio Configuration
AUDIO_CHUNK_SIZE = 2048
AUDIO_CHANNELS = 1
AUDIO_FORMAT = "paInt16"

# Servo Configuration
SERVO_DELAY = 0.001  # Delay between servo movements
SERVO_DIGITS = 3     # Precision for servo positions

# File Paths
LISTEN_SOUND_PATH = "Resources/listen.mp3"
CONVERT_SOUND_PATH = "Resources/convert.mp3"

# Serial Communication
SERIAL_BAUDRATE = 9600
SERIAL_TIMEOUT = 1
ARDUINO_PORT = "/dev/cu.usbmodem2101"  # Arduino port (update if different)

# Movement Configuration
DEFAULT_LEFT_SERVO_POS = 180   # Left arm default position
DEFAULT_RIGHT_SERVO_POS = 0    # Right arm default position
DEFAULT_HEAD_SERVO_POS = 90    # Head default position

# Hello Gesture Configuration
HELLO_WAVE_COUNT = 3           # Number of waves in hello gesture
HELLO_WAVE_DELAY = 0.2         # Delay between waves
