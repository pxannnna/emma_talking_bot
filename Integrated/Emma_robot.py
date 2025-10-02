

# ------------------- Import Libraries -------------------
import vosk
import pyaudio
import json
import pygame
import google.generativeai as genai
from openai import OpenAI
import io
import threading
import signal
from cvzone.SerialModule import SerialObject
from time import sleep
import sys
import os
# import keyboard  # type: ignore

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

# # ------------------- Initializations -------------------

# # Global exit event (immediate quit support)
# EXIT_NOW = threading.Event()

# def _signal_handler(signum, frame):
#     EXIT_NOW.set()

# # Handle Ctrl+C and termination signals
# signal.signal(signal.SIGINT, _signal_handler)
# try:
#     signal.signal(signal.SIGTERM, _signal_handler)
# except Exception:
#     pass

# # ------------------- Enhanced Keyboard Quit Functionality -------------------

# def keyboard_quit_listener():
#     """
#     Listen for keyboard combinations to quit the robot.
#     Supports: Ctrl+C, Ctrl+Q, Ctrl+Shift+Q, and Escape key
#     """
#     try:
#         # Listen for multiple quit combinations
#         keyboard.add_hotkey('ctrl+c', lambda: _trigger_quit("Ctrl+C"))
#         keyboard.add_hotkey('ctrl+q', lambda: _trigger_quit("Ctrl+Q"))
#         keyboard.add_hotkey('ctrl+shift+q', lambda: _trigger_quit("Ctrl+Shift+Q"))
#         keyboard.add_hotkey('esc', lambda: _trigger_quit("Escape"))
        
#         print("🎮 Keyboard quit shortcuts enabled:")
#         print("   - Ctrl+C (standard interrupt)")
#         print("   - Ctrl+Q (quick quit)")
#         print("   - Ctrl+Shift+Q (force quit)")
#         print("   - Escape key (emergency quit)")
#         print("   - Type 'q' + Enter in terminal")
        
#         # Keep the listener running
#         while not EXIT_NOW.is_set():
#             sleep(0.1)
            
#     except Exception as e:
#         print(f"⚠️ Keyboard listener error: {e}")
#         print("Falling back to Ctrl+C only")

# def _trigger_quit(combination):
#     """Trigger quit sequence with graceful shutdown"""
#     if not EXIT_NOW.is_set():
#         print(f"\n🛑 Quit requested via {combination}")
#         print("Shutting down Emma robot gracefully...")
#         EXIT_NOW.set()

# def graceful_shutdown():
#     """Perform graceful shutdown of Emma robot"""
#     try:
#         print("🔄 Performing graceful shutdown...")
        
#         # Reset servos to default positions
#         print("📍 Resetting servos to default positions...")
#         try:
#             move_servo([DEFAULT_LEFT_SERVO_POS, DEFAULT_RIGHT_SERVO_POS, DEFAULT_HEAD_SERVO_POS])
#         except Exception as e:
#             print(f"⚠️ Servo reset failed: {e}")
        
#         # Play goodbye sound
#         print("🔊 Playing goodbye sound...")
#         try:
#             play_sound(CONVERT_SOUND_PATH)
#         except Exception as e:
#             print(f"⚠️ Goodbye sound failed: {e}")
        
#         # Clean up Arduino connection
#         print("🔌 Closing Arduino connection...")
#         try:
#             arduino.close()
#         except Exception:
#             pass
            
#         print("✅ Emma robot shutdown complete!")
        
#     except Exception as e:
#         print(f"⚠️ Error during shutdown: {e}")
#         print("Force exiting...")

# ------------------- Servo Movements

# Create a Serial object with three digits precision for sending servo angles
# This works with cvzone SerialData format (3 values, 3 digits each)
# Use explicit port to ensure reliable connection
arduino = SerialObject(digits=SERVO_DIGITS, portNo=ARDUINO_PORT)

# Initialize the last known positions for the three servos: Left (LServo), Right (RServo), Head (HServo)
# LServo starts at 180 degrees, RServo at 0 degrees, and HServo at 90 degrees
last_positions = [DEFAULT_LEFT_SERVO_POS, DEFAULT_RIGHT_SERVO_POS, DEFAULT_HEAD_SERVO_POS]

# ------------------- AI speech integration portion
# Initialize Pygame mixer
pygame.mixer.init()

# Initialize VOSK model
model = vosk.Model(VOSK_MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, VOSK_SAMPLE_RATE)

# Configure Gemini API with your API key
genai.configure(api_key=GEMINI_API_KEY)

# Configure OpenAI Text-to-Speech API (ChatGPT Quality)
client = OpenAI(api_key=OPENAI_API_KEY)
print(f"Using OpenAI TTS with voice: {OPENAI_TTS_VOICE}")


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

# Play a startup sound once when the program begins
try:
    play_sound(LISTEN_SOUND_PATH)
except Exception:
    pass

# ------------------- Speech-to-Text Function -------------------

def listen_with_vosk():
    """
    Captures audio from the microphone and converts it to text using VOSK.

    Returns:
        str: Transcribed text from speech.
    """
    mic = pyaudio.PyAudio()  # Initialize microphone
    stream = mic.open(
        format=pyaudio.paInt16,
        channels=AUDIO_CHANNELS,
        rate=VOSK_SAMPLE_RATE,
        input=True,
        frames_per_buffer=AUDIO_CHUNK_SIZE,
        start=False
    )
    stream.start_stream()
    print("Listening ...")

    while True:
        if EXIT_NOW.is_set():
            try:
                if stream.is_active():
                    stream.stop_stream()
            except Exception:
                pass
            try:
                stream.close()
            except Exception:
                pass
            try:
                mic.terminate()
            except Exception:
                pass
            raise SystemExit(0)
        try:
            data = stream.read(AUDIO_CHUNK_SIZE, exception_on_overflow=False)
        except Exception:
            continue
        if len(data) == 0:  # Skip if no audio data
            continue

        if recognizer.AcceptWaveform(data):  # Recognize speech
            result = recognizer.Result()  # Get result from recognizer
            text = json.loads(result)["text"]  # Extract text
            print("You said: " + text)
            # Clean up audio resources before returning
            try:
                if stream.is_active():
                    stream.stop_stream()
            except Exception:
                pass
            try:
                stream.close()
            except Exception:
                pass
            try:
                mic.terminate()
            except Exception:
                pass
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

def openai_text_to_speech(text):
    """
    Converts input text to speech using OpenAI's Text-to-Speech API (ChatGPT Quality).

    Args:
        text (str): Text to convert to speech.

    Returns:
        bytes: Binary audio content generated by the API.
    """
    # Generate speech
    response = client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=OPENAI_TTS_VOICE,
        input=text
    )
    # Extract audio content from the response
    audio_content = response.read()  # Read the binary content
    return audio_content

def play_audio(audio_bytes):
    """
    Plays audio content using pygame.

    Args:
        audio_bytes (bytes): Binary audio content to play.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(io.BytesIO(audio_bytes))  # Load audio from bytes
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for playback to finish
        pygame.time.Clock().tick(10)

def text_to_speech(text):
    """
    Converts input text to speech and plays it.

    Args:
        text (str): Text to convert to speech.
    """
    print(f"Emma says: {text}")
    audio_content = openai_text_to_speech(text)
    play_audio(audio_content)


# ------------------- Movement Functions -------------------

# Function to smoothly move servos to target positions
def move_servo(target_positions, delay=SERVO_DELAY):
    """
    Moves the servos smoothly to the target positions.

    :param target_positions: List of target angles [LServo, RServo, HServo]
    :param delay: Time delay (in seconds) between each incremental step
    """
    global last_positions  # Use the global variable to track servo positions
    # Calculate the maximum number of steps required for the largest position difference
    max_steps = max(abs(target_positions[i] - last_positions[i]) for i in range(3))

    # Incrementally move each servo to its target position over multiple steps
    for step in range(max_steps):
        # Calculate the current position of each servo at this step
        current_positions = [
            last_positions[i] + (step + 1) * (target_positions[i] - last_positions[i]) // max_steps
            if abs(target_positions[i] - last_positions[i]) > step else last_positions[i]
            for i in range(3)
        ]
        # Send the calculated positions to the Arduino
        arduino.sendData(current_positions)
        # Introduce a small delay to ensure smooth motion
        sleep(delay)

    # Update the last known positions to the target positions
    last_positions = target_positions[:]


def hello_gesture():
    """
    Makes Emma wave hello by moving the right servo back and forth.
    """
    global last_positions
    # Move right arm to start waving
    move_servo([last_positions[0], 180, last_positions[2]])
    for _ in range(HELLO_WAVE_COUNT):  # Perform the waving motion
        move_servo([last_positions[0], 150, last_positions[2]])  # Move arm slightly down
        move_servo([last_positions[0], 180, last_positions[2]])  # Move arm back up
    # Reset arm to original position
    move_servo([last_positions[0], 0, last_positions[2]])


# New: Left-hand goodbye gesture (distinct from right-hand hello)
def goodbye_gesture():
    """
    Waves goodbye using the left servo (opposite hand from hello).
    """
    global last_positions
    # Raise left arm to start waving (left up is near 0)
    move_servo([0, last_positions[1], last_positions[2]])
    for _ in range(HELLO_WAVE_COUNT):  # reuse wave count for symmetry
        move_servo([30, last_positions[1], last_positions[2]])  # slight down
        move_servo([0, last_positions[1], last_positions[2]])   # back up
    # Reset left arm to original position (default 180)
    move_servo([DEFAULT_LEFT_SERVO_POS, last_positions[1], last_positions[2]])


# New: speaking hand control (use left hand for speaking)
def raise_speaking_hand():
    """Raise the left arm while speaking."""
    global last_positions
    move_servo([0, last_positions[1], last_positions[2]])


def lower_speaking_hand():
    """Lower the left arm when listening/idle."""
    global last_positions
    move_servo([DEFAULT_LEFT_SERVO_POS, last_positions[1], last_positions[2]])


# New: head positioning helpers
def set_head(angle_deg):
    """Move only the head to the specified angle."""
    global last_positions
    move_servo([last_positions[0], last_positions[1], angle_deg])


def set_head_listening():
    """Head turned to 45° while listening."""
    set_head(45)


def set_head_speaking():
    """Head straight (90°) while speaking."""
    set_head(90)

# ------------------- Main Loop -------------------

EXIT_KEYWORDS = {"stop", "quit", "goodbye", "exit", "bye"}

# # Background stdin watcher: type 'q' (or 'quit'/'exit') + Enter to quit immediately
# def _stdin_quit_watcher():
#     try:
#         while not EXIT_NOW.is_set():
#             line = input()
#             if line is None:
#                 continue
#             if line.strip().lower() in {"q", "quit", "exit"}:
#                 _trigger_quit("Terminal input")
#                 break
#     except Exception:
#         # If stdin is not interactive, just ignore
#         pass

# # Start keyboard listener thread
# keyboard_thread = threading.Thread(target=keyboard_quit_listener, daemon=True)
# keyboard_thread.start()

# # Start stdin watcher thread
# _stdin_thread = threading.Thread(target=_stdin_quit_watcher, daemon=True)
# _stdin_thread.start()

while True:
    # if EXIT_NOW.is_set():
    #     break

    # Move Emma to casual gesture (head to 45° for listening)
    move_servo([DEFAULT_LEFT_SERVO_POS, DEFAULT_RIGHT_SERVO_POS, 45], delay=SERVO_DELAY)

    # Listen for speech input
    # Ensure speaking hand is lowered and head is in listening pose (45°)
    lower_speaking_hand()
    set_head_listening()
    # if EXIT_NOW.is_set():
    #     break
    text = listen_with_vosk()

    # Exit if stop keywords are spoken
    if any(k in text.lower() for k in EXIT_KEYWORDS):
        print("Exit phrase detected. Shutting down...")
        try:
            # Play a goodbye gesture with the left hand
            goodbye_gesture()
            text_to_speech("Goodbye!")
        except Exception:
            pass
        # EXIT_NOW.set()
        break

    # Waves if "hello Emma"
    if "hello" in text.lower() or "emma" in text.lower():
        print("Triggering Hello Gesture...")
        hello_gesture()

        response_text = "Hello! How can I assist you today?"
        # Raise speaking hand while talking
        raise_speaking_hand()
        set_head_speaking()
        text_to_speech(response_text)
        # Lower after speaking
        lower_speaking_hand()
        set_head_listening()

    # Normal conversation
    else:
        print(f"Processing input: {text}")
        ai_response = gemini_api(text)
        # Raise speaking hand while talking
        raise_speaking_hand()
        set_head_speaking()
        text_to_speech(ai_response)
        # Lower after speaking
        lower_speaking_hand()
        set_head_listening()

# # Perform graceful shutdown when exiting
# graceful_shutdown()
print("Emma Robot exited cleanly.")


