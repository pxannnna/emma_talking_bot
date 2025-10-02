# 🤖 Emma - The Talking Robot

Meet Emma, an intelligent conversational robot that combines cutting-edge AI with expressive physical movements. Emma can listen to your voice, understand what you're saying, generate intelligent responses using AI, and express herself through both speech and graceful servo-controlled gestures.

![Emma Robot](https://img.shields.io/badge/Status-Functional-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Arduino](https://img.shields.io/badge/Arduino-Compatible-orange)

## 🌟 What Makes Emma Special?

Emma is more than just a chatbot - she's a physical robot that:

- **Listens** using advanced offline speech recognition (VOSK)
- **Thinks** using Google's Gemini AI for intelligent conversations
- **Speaks** with natural, human-like voice (OpenAI TTS)
- **Moves** with expressive gestures using 3 servo motors
- **Learns** and responds contextually to different types of interactions

### 🎭 Emma's Personality & Gestures

- **Hello Gesture**: Waves enthusiastically when greeted
- **Speaking Pose**: Raises her left hand while talking
- **Listening Pose**: Tilts her head and lowers her speaking hand
- **Goodbye Gesture**: Waves farewell with her left hand
- **Dynamic Head Movement**: Follows conversation flow with head positioning

## 🏗️ Technical Architecture

Emma's intelligence is built on a sophisticated multi-layer architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                       │
│              (Voice Input/Output)                       │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│              Speech Processing Layer                    │
│  • VOSK (Offline Speech Recognition)                   │
│  • OpenAI TTS (Natural Voice Generation)               │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                AI Processing Layer                      │
│  • Google Gemini AI (Conversation Intelligence)        │
│  • Context-aware response generation                    │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│              Physical Control Layer                     │
│  • Arduino + PCA9685 (Servo Control)                   │
│  • 3 Servo Motors (Left Arm, Right Arm, Head)          │
│  • Smooth gesture animations                            │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Hardware Requirements

### Core Components
- **Arduino Uno/Nano** - Main microcontroller
- **PCA9685 PWM Servo Driver** - 16-channel servo controller
- **3x Servo Motors** - For expressive movements
- **Microphone** - Voice input
- **Speakers** - Audio output
- **Power Supply** - 5V for servos (external recommended)

### Connection Diagram
```
Arduino ←→ PCA9685 ←→ Servos
   │           │         │
   │           │         ├─ Left Arm (Channel 1)
   │           │         ├─ Right Arm (Channel 2)
   │           │         └─ Head (Channel 3)
   │           │
   │           └─ I2C (SDA→A4, SCL→A5)
   │
   └─ USB ←→ Computer (Python Control)
```

## 🚀 Quick Start Guide

### 1. Hardware Setup (15 minutes)

1. **Connect PCA9685 to Arduino**:
   - SDA → A4, SCL → A5
   - VCC → 5V, GND → GND

2. **Connect Servos to PCA9685**:
   - Left Arm → Channel 1
   - Right Arm → Channel 2  
   - Head → Channel 3

3. **Upload Arduino Code**:
   ```bash
   # Open Arduino IDE
   # Load: Arduino/emma_servo_control/emma_servo_control.ino
   # Upload to your Arduino
   ```

### 2. Software Setup (10 minutes)

1. **Install Python Dependencies**:
   ```bash
   pip install -r req.txt
   pip install keyboard  # For enhanced quit functionality
   ```

2. **Configure API Keys**:
   ```bash
   cp config_template.py config.py
   # Edit config.py with your API keys:
   # - Google Gemini API (free tier available)
   # - OpenAI API (for natural voice)
   ```

### 3. Launch Emma (30 seconds)

```bash
python3 Integrated/Emma_robot.py
```

**Emma will greet you and start listening!** 🎉

## 💬 How to Interact with Emma

### Voice Commands
- **"Hello Emma"** → Triggers hello gesture + greeting
- **"Goodbye"** / **"Stop"** → Emma waves goodbye and shuts down
- **Any question** → Emma thinks, gestures, and responds intelligently

### Example Conversations
```
You: "Hello Emma, how are you today?"
Emma: *waves* "Hello! I'm doing great, thank you for asking. How can I assist you today?"

You: "What's the weather like?"
Emma: *raises speaking hand* "I don't have access to real-time weather data, but I'd be happy to help you find weather information for your location!"

You: "Tell me a joke"
Emma: *head movement* "Why don't scientists trust atoms? Because they make up everything!"
```

## 🎛️ Advanced Features

### Gesture System
Emma's movement system is designed for natural expression:

- **Smooth Animations**: Servos move incrementally for fluid motion
- **Contextual Gestures**: Different movements for different conversation states
- **Head Tracking**: Follows conversation flow with head positioning
- **Asymmetric Design**: Left hand for speaking, right hand for greetings

### AI Integration
- **Gemini AI**: State-of-the-art conversational AI
- **OpenAI TTS**: Natural, human-like voice synthesis
- **Offline Speech**: VOSK for privacy-conscious voice recognition
- **Context Awareness**: Maintains conversation context

### Safety & Reliability
- **Graceful Shutdown**: Proper servo reset on exit
- **Error Handling**: Robust error recovery
- **Keyboard Shortcuts**: Multiple ways to safely quit
- **Resource Management**: Proper cleanup of audio and serial resources

## 🛠️ Development & Customization

### Project Structure
```
emma_talking_bot/
├── Integrated/           # Main robot code
│   └── Emma_robot.py    # Complete Emma implementation
├── Arduino/             # Hardware control
│   └── emma_servo_control/ # Servo control firmware
├── Software/            # Individual components
│   ├── AI_model.py      # Gemini AI integration
│   ├── Speech_to_text_offline.py # VOSK recognition
│   └── text_to_speech.py # OpenAI TTS
├── Hardware/            # Hardware testing
├── Resources/           # Audio files & models
└── config_template.py   # Configuration template
```

### Adding New Gestures

1. **Arduino Side**: Add new movement patterns in `emma_servo_control.ino`
2. **Python Side**: Create new gesture functions in `Emma_robot.py`
3. **Integration**: Link gestures to specific conversation triggers

Example:
```python
def excited_gesture():
    """Emma gets excited with rapid head movement"""
    for _ in range(3):
        move_servo([last_positions[0], last_positions[1], 45])
        sleep(0.2)
        move_servo([last_positions[0], last_positions[1], 135])
        sleep(0.2)
```

### Customizing AI Responses

Modify the AI prompt system in `gemini_api()` function:
```python
def gemini_api(text):
    # Add personality modifiers
    prompt = f"Respond as Emma, a friendly robot assistant. Keep responses concise and engaging: {text}"
    # ... rest of implementation
```

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Emma doesn't move | Check Arduino connection and servo power |
| Speech not recognized | Verify microphone permissions and VOSK model |
| API errors | Confirm API keys and internet connection |
| Servos jittery | Ensure stable 5V power supply |
| Audio delays | Check audio buffer settings |

### Debug Mode
Enable verbose logging by modifying the main loop:
```python
# Add debug prints to track conversation flow
print(f"Processing: {text}")
print(f"AI Response: {ai_response}")
```

## 📊 Performance Specifications

- **Speech Recognition**: ~2-3 second latency (VOSK offline)
- **AI Response**: ~1-2 seconds (Gemini API)
- **Text-to-Speech**: ~1-2 seconds (OpenAI TTS)
- **Servo Movement**: ~0.5-1 second per gesture
- **Total Response Time**: ~4-8 seconds end-to-end

## 🔐 Security & Privacy

- **Local Speech Recognition**: VOSK runs entirely offline
- **API Keys**: Protected by `.gitignore` and environment variables
- **No Data Storage**: Conversations are not saved or logged
- **Secure Configuration**: Template-based setup prevents key exposure

## 🌟 Future Enhancements

Potential improvements for Emma:

- **Computer Vision**: Add camera for visual recognition
- **More Servos**: Expand to full body movement
- **Personality Learning**: Adaptive conversation style
- **Home Integration**: Smart home control capabilities
- **Mobile App**: Remote control and monitoring

## 📚 Educational Value

Emma is perfect for learning:

- **Robotics**: Servo control and physical computing
- **AI Integration**: Modern AI APIs and natural language processing
- **Python Programming**: Multi-threading, serial communication, audio processing
- **Arduino Development**: I2C communication, PWM control
- **System Integration**: Connecting multiple technologies

## 🤝 Contributing

Emma is an open educational project! Feel free to:

- Add new gestures and personality traits
- Improve speech recognition accuracy
- Enhance AI conversation capabilities
- Optimize hardware performance
- Create documentation and tutorials

## 📄 License

This project is for educational purposes. Please ensure compliance with:
- OpenAI Terms of Service
- Google AI Terms of Service
- VOSK Model License
- Arduino IDE License

---

**Made with ❤️ for the robotics and AI community**

*Emma represents the future of human-robot interaction - where AI meets physical expression to create truly engaging conversational experiences.*