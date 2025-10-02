#!/usr/bin/env python3
"""
Test script for servo communication with PCA9685
Tests the communication between Python and Arduino without requiring full robot functionality
"""

import sys
import os
import time

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_servo_communication():
    """Test basic servo communication"""
    print("Testing servo communication with PCA9685...")
    
    try:
        from cvzone.SerialModule import SerialObject
        from config import ARDUINO_PORT, SERVO_DIGITS
        
        # Create serial object with explicit port
        arduino = SerialObject(digits=SERVO_DIGITS, portNo=ARDUINO_PORT)
        print("✓ SerialObject created successfully")
        
        # Test positions
        test_positions = [
            [180, 0, 90],    # Default positions
            [90, 90, 90],    # Center positions
            [0, 180, 45],    # Different positions
            [180, 0, 90],    # Back to default
        ]
        
        print("Sending test positions to servos...")
        for i, positions in enumerate(test_positions):
            print(f"  Test {i+1}: Left={positions[0]}, Right={positions[1]}, Head={positions[2]}")
            arduino.sendData(positions)
            time.sleep(2)  # Wait for movement to complete
        
        print("✓ Servo communication test completed successfully!")
        print("If you see servo movements, the communication is working correctly.")
        
        return True
        
    except Exception as e:
        print(f"✗ Servo communication test failed: {e}")
        print("Make sure:")
        print("1. Arduino is connected and running the servo control code")
        print("2. PCA9685 is properly connected")
        print("3. Servos are connected to channels 0, 1, 2")
        return False

def main():
    """Run servo communication test"""
    print("Emma Robot - Servo Communication Test")
    print("=" * 50)
    
    success = test_servo_communication()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Servo communication test passed!")
        print("Your PCA9685 setup is working correctly.")
    else:
        print("❌ Servo communication test failed.")
        print("Please check your hardware connections and Arduino code.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
