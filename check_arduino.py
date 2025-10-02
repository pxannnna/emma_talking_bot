#!/usr/bin/env python3
"""
Simple Arduino connection checker
Run this anytime to check if Arduino is connected
"""

import serial.tools.list_ports
from cvzone.SerialModule import SerialObject
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import ARDUINO_PORT

def check_arduino_connection():
    """Check if Arduino is connected and responding"""
    print("🔍 Arduino Connection Checker")
    print("=" * 40)
    
    # Check if port exists
    ports = serial.tools.list_ports.comports()
    port_found = False
    
    for port in ports:
        if port.device == ARDUINO_PORT:
            port_found = True
            print(f"✅ Port found: {ARDUINO_PORT}")
            break
    
    if not port_found:
        print(f"❌ Port not found: {ARDUINO_PORT}")
        print("Available ports:")
        for port in ports:
            print(f"  - {port.device}: {port.description}")
        return False
    
    # Try to connect
    try:
        print(f"🔌 Attempting to connect to {ARDUINO_PORT}...")
        arduino = SerialObject(digits=3, portNo=ARDUINO_PORT)
        print("✅ Arduino is CONNECTED and responding!")
        
        # Test communication
        print("📤 Testing communication...")
        arduino.sendData([90, 90, 90])
        print("✅ Communication test successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    if check_arduino_connection():
        print("\n🎉 Arduino is ready to use!")
    else:
        print("\n🚨 Arduino connection failed!")
        print("Check:")
        print("1. USB cable is connected")
        print("2. Arduino is powered on")
        print("3. Arduino code is uploaded")
        print("4. No other programs are using the port")
