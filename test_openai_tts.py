#!/usr/bin/env python3
"""
Test script for OpenAI TTS functionality
Tests the ChatGPT-quality voice system
"""

import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_openai_tts():
    """Test the OpenAI TTS functionality"""
    print("Testing OpenAI TTS (ChatGPT Quality)...")
    
    try:
        from openai import OpenAI
        import pygame
        import io
        print("✓ OpenAI and pygame imported successfully")
        
        # Import config
        import config
        
        if config.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
            print("❌ OpenAI API key not configured!")
            print("Please get an API key from https://platform.openai.com/")
            print("and update config.py")
            return False
        
        # Initialize OpenAI client
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        print("✓ OpenAI client initialized")
        
        # Test TTS
        test_text = "Hello! I am Emma, your personal AI robot. I now sound just like ChatGPT!"
        print(f"Generating speech: {test_text}")
        
        response = client.audio.speech.create(
            model=config.OPENAI_TTS_MODEL,
            voice=config.OPENAI_TTS_VOICE,
            input=test_text
        )
        
        print("✓ Speech generated successfully")
        
        # Play the audio
        audio_content = response.read()
        pygame.mixer.init()
        pygame.mixer.music.load(io.BytesIO(audio_content))
        pygame.mixer.music.play()
        
        print("🎵 Playing ChatGPT-quality voice...")
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        print("✓ OpenAI TTS test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ OpenAI TTS test failed: {e}")
        return False

def main():
    """Run OpenAI TTS test"""
    print("Emma Robot - OpenAI TTS Test")
    print("=" * 40)
    
    success = test_openai_tts()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 OpenAI TTS test passed!")
        print("Emma now sounds just like ChatGPT! 🎤✨")
        print("\n💡 Cost estimate:")
        print("- Typical usage: ~$0.30/month")
        print("- Very affordable for ChatGPT-quality voice!")
    else:
        print("❌ OpenAI TTS test failed.")
        print("Please check your OpenAI API key in config.py")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
