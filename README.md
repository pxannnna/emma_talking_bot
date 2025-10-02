# Emma Talking Bot - Robot Project

This is a Python-based robot project that integrates speech recognition, AI text generation, and text-to-speech capabilities with servo motor control for a physical robot named Emma.

## Project Structure

```
emma_talking_bot/
├── Arduino/                    # Arduino code for servo control
│   └── emma_servo_control.ino # Main Arduino sketch
├── Hardware/                   # Hardware control scripts
│   ├── Hello_emma.py          # Hello gesture demonstration
│   └── Servos_basic.py        # Basic servo movement
├── Integrated/                 # Main integrated robot code
│   └── Emma_robot.py          # Complete robot integration
├── Software/                   # Individual software components
│   ├── AI_model.py            # Gemini AI integration
│   ├── AI_speech_integration.py # Complete AI-speech pipeline
│   ├── Speech_to_text.py      # Google Speech Recognition
│   ├── Speech_to_text_offline.py # VOSK offline speech recognition
│   ├── text_to_speech.py      # OpenAI TTS
│   └── text_to_speech_offline.py # Offline TTS with pyttsx3
├── Resources/                  # Audio files and VOSK models
│   ├── listen.mp3             # Listening prompt sound
│   ├── convert.mp3            # Processing prompt sound
│   └── vosk-model-en-us-0.22/ # VOSK speech recognition model
├── main.py                     # Simple test file
├── req.txt                     # Python dependencies
└── README.md                   # This file
```

## Prerequisites

### Hardware Requirements
- Arduino board (Uno, Nano, or similar)
- PCA9685 PWM Servo Driver Shield (16-channel)
- 3 servo motors (for left arm, right arm, and head)
- Microphone for speech input
- Speakers/headphones for audio output
- USB cable to connect Arduino to computer
- Jumper wires for connections

### Software Requirements
- Python 3.8 or higher
- Arduino IDE
- Internet connection (for AI APIs)

## Setup Instructions

### 1. Arduino Setup

1. **Install Arduino IDE** from [arduino.cc](https://www.arduino.cc/en/software)

2. **Install required libraries** in Arduino IDE:
   - Go to Tools → Manage Libraries
   - Search for and install:
     - "Adafruit PWM Servo Driver Library" by Adafruit
     - "cvzone" by Murtaza Hassan (for SerialData communication)

3. **Hardware connections**:
   - Connect PCA9685 shield to Arduino (I2C pins: SDA to A4, SCL to A5)
   - Connect servos to PCA9685 channels:
     - Left servo to channel 0
     - Right servo to channel 1  
     - Head servo to channel 2
   - Power PCA9685 with appropriate power supply (5V recommended)
   - **Important**: Don't power servos from Arduino USB - use external power supply

4. **Upload code**:
   - Open `Arduino/emma_servo_control/emma_servo_control.ino` in Arduino IDE
   - Select correct board and port
   - Click Upload
   - Open Serial Monitor to verify "Emma Robot Servo Control Ready with PCA9685" message

### 2. Python Environment Setup

1. **Create virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r req.txt
   ```

3. **Install additional dependencies** (if needed):
   ```bash
   pip install opencv-python
   ```

### 3. API Keys Setup

**IMPORTANT**: You need two API keys for the best experience:

1. **Google Gemini API** (Free tier available):
   - Go to [Google AI Studio](https://ai.google.dev/)
   - Create an API key (free tier: 15 requests/minute, 1M tokens/day)
   - Replace the key in `config.py`

2. **OpenAI API** (For ChatGPT-quality voice):
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Create an API key
   - Replace the key in `config.py`
   - Cost: ~$0.30/month for typical usage

### 4. Audio Setup

1. **Test microphone access**:
   ```bash
   python3 -c "import pyaudio; print('Microphone access OK')"
   ```

2. **Test audio output**:
   ```bash
   python3 -c "import pygame; print('Audio output OK')"
   ```

## Usage

### Basic Testing

1. **Test servos** (without Arduino):
   ```bash
   python3 Hardware/Servos_basic.py
   ```

2. **Test speech recognition**:
   ```bash
   python3 Software/Speech_to_text_offline.py
   ```

3. **Test AI integration**:
   ```bash
   python3 Software/AI_model.py
   ```

### Full Robot Operation

1. **Ensure Arduino is connected** and running the servo control code
2. **Run the main robot**:
   ```bash
   python3 Integrated/Emma_robot.py
   ```

3. **Interact with Emma**:
   - Say "hello Emma" to trigger the hello gesture
   - Ask questions for AI responses
   - The robot will respond with speech and movement

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure virtual environment is activated
   - Check all dependencies are installed: `pip list`

2. **Microphone Access Issues** (macOS):
   - Go to System Preferences → Security & Privacy → Privacy → Microphone
   - Ensure your terminal/IDE has microphone access

3. **Serial Communication Errors**:
   - Check Arduino is connected and port is correct
   - Verify Arduino code is uploaded successfully
   - Check serial monitor for error messages

4. **VOSK Model Issues**:
   - Ensure VOSK model files are in the correct location
   - Check model path in code matches actual file structure

5. **API Key Errors**:
   - Verify both Gemini and OpenAI API keys are correct
   - Check internet connection (needed for both APIs)
   - Ensure sufficient credits in OpenAI account

### Hardware Issues

1. **Servos not moving**:
   - Check PCA9685 power supply (5V recommended)
   - Verify I2C connections (SDA to A4, SCL to A5)
   - Check servo connections to PCA9685 channels (0, 1, 2)
   - Ensure Adafruit PWM library is installed
   - Check serial communication in Arduino IDE Serial Monitor

2. **Erratic servo movement**:
   - Ensure stable power supply for PCA9685
   - Check for loose connections
   - Verify servo specifications (voltage, current)
   - Adjust SERVO_MIN_TICKS and SERVO_MAX_TICKS in Arduino code if needed

3. **PCA9685 not detected**:
   - Check I2C connections
   - Verify power supply to PCA9685
   - Try different I2C address if using multiple devices

### Performance Issues

1. **Slow speech recognition**:
   - VOSK models can be slow on older hardware
   - Consider using smaller VOSK model
   - Use Google Speech Recognition for better performance (requires internet)

2. **Audio delays**:
   - Check audio buffer settings
   - Ensure sufficient CPU resources

## Customization

### Adding New Gestures

1. **Modify Arduino code** to add new servo movements
2. **Update Python code** to trigger new gestures
3. **Test thoroughly** to ensure smooth movement

### Changing AI Model

1. **Replace Gemini API** with other AI services
2. **Modify response processing** as needed
3. **Update voice settings** for different TTS services

### Hardware Modifications

1. **Add more servos** by extending Arduino code (PCA9685 supports up to 16 servos)
2. **Change servo channels** in Arduino code (CH_LEFT, CH_RIGHT, CH_HEAD constants)
3. **Add sensors** for more interactive behavior
4. **Adjust servo pulse ranges** by modifying SERVO_MIN_TICKS and SERVO_MAX_TICKS

## Safety Notes

- **Power PCA9685 separately** from Arduino to avoid damage
- **Use appropriate power supply** for your servo specifications (5V recommended)
- **Test movements slowly** to avoid mechanical damage
- **Keep hands clear** of moving parts during testing
- **Check servo pulse ranges** before connecting to avoid damage

## Support

For issues related to:
- **Python code**: Check import statements and dependencies
- **Arduino code**: Verify wiring and servo connections
- **API services**: Check API keys and internet connectivity
- **Hardware**: Ensure proper power supply and connections

## License

This project is for educational purposes. Please ensure you comply with the terms of service for any third-party APIs used.
