#!/usr/bin/env python3
"""
Proper Arduino connection test that actually verifies communication
"""

import serial
import serial.tools.list_ports
import time

def find_arduino_port():
    """Find Arduino port by checking for common Arduino identifiers"""
    ports = serial.tools.list_ports.comports()
    
    for port in ports:
        # Check for common Arduino identifiers
        if any(identifier in port.description.lower() for identifier in 
               ['arduino', 'usb serial', 'ch340', 'cp210', 'ftdi']):
            return port.device
    
    return None

def test_arduino_connection():
    """Test actual Arduino connection with proper error handling"""
    print("🔍 Searching for Arduino...")
    
    # Find Arduino port
    arduino_port = find_arduino_port()
    
    if not arduino_port:
        print("❌ No Arduino found!")
        print("Available ports:")
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print(f"  - {port.device}: {port.description}")
        return False
    
    print(f"✅ Found Arduino on: {arduino_port}")
    
    try:
        # Try to connect with proper baud rate
        print("🔌 Attempting to connect at 9600 baud...")
        ser = serial.Serial(arduino_port, 9600, timeout=2)
        time.sleep(2)  # Wait for Arduino to initialize
        
        # Clear any existing data
        ser.flushInput()
        ser.flushOutput()
        
        # Wait for Arduino startup message
        print("⏳ Waiting for Arduino startup message...")
        time.sleep(3)
        
        # Read any available data
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print("📥 Arduino startup message:")
            print(data)
        else:
            print("⚠️  No startup message received")
        
        # Test sending a simple command
        print("📤 Testing command: [90,90,90]")
        ser.write(b"090090090")  # Send 3-digit format
        time.sleep(1)
        
        # Check for response
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print("📥 Arduino response:")
            print(response)
        else:
            print("⚠️  No response received")
        
        ser.close()
        return True
        
    except serial.SerialException as e:
        print(f"❌ Serial connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_cvzone_connection():
    """Test cvzone connection with proper error handling"""
    print("\n🔍 Testing cvzone SerialObject...")
    
    try:
        from cvzone.SerialModule import SerialObject
        
        # Try to create SerialObject
        arduino = SerialObject(digits=3)
        
        # Test if we can actually send data
        print("📤 Sending test command: [90,90,90]")
        arduino.sendData([90, 90, 90])
        
        print("✅ cvzone connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ cvzone connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Proper Arduino Connection Test")
    print("=" * 40)
    
    # Test 1: Direct serial connection
    serial_ok = test_arduino_connection()
    
    # Test 2: cvzone connection
    cvzone_ok = test_cvzone_connection()
    
    print("\n📊 Results:")
    print(f"Direct Serial: {'✅ OK' if serial_ok else '❌ FAILED'}")
    print(f"cvzone SerialObject: {'✅ OK' if cvzone_ok else '❌ FAILED'}")
    
    if not serial_ok and not cvzone_ok:
        print("\n🚨 No working connection found!")
        print("Check:")
        print("1. Arduino is connected via USB")
        print("2. Arduino code is uploaded")
        print("3. Correct COM port is being used")
        print("4. No other programs are using the serial port")


