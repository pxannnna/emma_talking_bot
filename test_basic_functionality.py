#!/usr/bin/env python3
"""
Test script for Emma Robot Project
Tests basic functionality without requiring hardware
"""

import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required libraries can be imported"""
    print("Testing imports...")
    
    try:
        import vosk
        print("✓ VOSK imported successfully")
    except ImportError as e:
        print(f"✗ VOSK import failed: {e}")
        return False
    
    try:
        import pyaudio
        print("✓ PyAudio imported successfully")
    except ImportError as e:
        print(f"✗ PyAudio import failed: {e}")
        return False
    
    try:
        import pygame
        print("✓ Pygame imported successfully")
    except ImportError as e:
        print(f"✗ Pygame import failed: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✓ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"✗ Google Generative AI import failed: {e}")
        return False
    
    try:
        from openai import OpenAI
        print("✓ OpenAI TTS imported successfully")
    except ImportError as e:
        print(f"✗ OpenAI import failed: {e}")
        return False
    
    try:
        from cvzone.SerialModule import SerialObject
        print("✓ CVZone SerialModule imported successfully")
    except ImportError as e:
        print(f"✗ CVZone SerialModule import failed: {e}")
        return False
    
    return True

def test_vosk_model():
    """Test if VOSK model can be loaded"""
    print("\nTesting VOSK model...")
    
    try:
        import vosk
        model = vosk.Model("Resources/vosk-model-en-us-0.22")
        print("✓ VOSK model loaded successfully")
        return True
    except Exception as e:
        print(f"✗ VOSK model loading failed: {e}")
        return False

def test_audio_files():
    """Test if audio files exist"""
    print("\nTesting audio files...")
    
    audio_files = [
        "Resources/listen.mp3",
        "Resources/convert.mp3"
    ]
    
    all_exist = True
    for file_path in audio_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_config():
    """Test if configuration can be imported"""
    print("\nTesting configuration...")
    
    try:
        import config
        print("✓ Configuration imported successfully")
        
        # Check if API keys are set
        if config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            print("⚠ Gemini API key not configured")
        else:
            print("✓ Gemini API key configured")
            
        if config.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
            print("⚠ OpenAI API key not configured")
        else:
            print("✓ OpenAI API key configured")
            
        print("✓ Using OpenAI TTS (ChatGPT quality voice)")
            
        return True
    except ImportError as e:
        print(f"✗ Configuration import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_serial_simulation():
    """Test serial communication simulation"""
    print("\nTesting serial communication simulation...")
    
    try:
        from cvzone.SerialModule import SerialObject
        
        # Try to create a serial object (will fail without actual device, but should not crash)
        try:
            arduino = SerialObject(digits=3)
            print("✓ SerialObject created successfully")
        except Exception as e:
            print(f"⚠ SerialObject created but may not connect to device: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Serial communication test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Emma Robot Project - Basic Functionality Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_vosk_model,
        test_audio_files,
        test_config,
        test_serial_simulation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The project should work correctly.")
        print("\nNext steps:")
        print("1. Configure your API keys in config.py:")
        print("   - Gemini API key (free tier available)")
        print("   - OpenAI API key (for ChatGPT-quality voice)")
        print("2. Connect Arduino with servo motors")
        print("3. Run Integrated/Emma_robot.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("1. Activate virtual environment: source .venv/bin/activate")
        print("2. Install missing dependencies: pip install -r req.txt")
        print("3. Check file paths and permissions")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
