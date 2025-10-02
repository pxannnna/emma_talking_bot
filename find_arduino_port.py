#!/usr/bin/env python3
"""
Find Arduino port and test connection
"""

import serial.tools.list_ports
import serial
import time

def find_arduino_ports():
    """Find all potential Arduino ports"""
    print("🔍 Scanning for Arduino ports...")
    
    ports = serial.tools.list_ports.comports()
    arduino_ports = []
    
    for port in ports:
        print(f"Found: {port.device} - {port.description}")
        
        # Check for Arduino identifiers
        if any(identifier in port.description.lower() for identifier in 
               ['arduino', 'usb serial', 'ch340', 'cp210', 'ftdi']):
            arduino_ports.append(port.device)
            print(f"  ✅ Likely Arduino: {port.device}")
        elif 'usbmodem' in port.device.lower():
            arduino_ports.append(port.device)
            print(f"  ✅ USB Serial (likely Arduino): {port.device}")
    
    return arduino_ports

def test_port_connection(port):
    """Test connection to a specific port"""
    print(f"\n🔌 Testing connection to {port}...")
    
    try:
        ser = serial.Serial(port, 9600, timeout=2)
        time.sleep(2)
        
        # Clear buffers
        ser.flushInput()
        ser.flushOutput()
        
        # Wait for Arduino startup
        time.sleep(3)
        
        # Read startup message
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f"📥 Startup message from {port}:")
            print(data)
        
        # Test sending command
        print(f"📤 Sending test command to {port}...")
        ser.write(b"090090090")
        time.sleep(1)
        
        # Read response
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f"📥 Response from {port}:")
            print(response)
        
        ser.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to {port}: {e}")
        return False

def test_cvzone_with_port(port):
    """Test cvzone SerialObject with specific port"""
    print(f"\n🔧 Testing cvzone with port {port}...")
    
    try:
        from cvzone.SerialModule import SerialObject
        
        # Try with explicit port
        arduino = SerialObject(digits=3, port=port)
        print(f"✅ cvzone connected to {port}!")
        
        # Test sending data
        print("📤 Sending test command: [90, 90, 90]")
        arduino.sendData([90, 90, 90])
        time.sleep(2)
        
        print("📤 Sending test command: [180, 0, 90]")
        arduino.sendData([180, 0, 90])
        time.sleep(2)
        
        print("✅ cvzone test successful!")
        return True
        
    except Exception as e:
        print(f"❌ cvzone test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Arduino Port Finder and Tester")
    print("=" * 50)
    
    # Find all potential Arduino ports
    arduino_ports = find_arduino_ports()
    
    if not arduino_ports:
        print("\n❌ No Arduino ports found!")
        print("Make sure:")
        print("1. Arduino is connected via USB")
        print("2. Arduino drivers are installed")
        print("3. Arduino is powered on")
        exit()
    
    print(f"\n🎯 Found {len(arduino_ports)} potential Arduino port(s):")
    for port in arduino_ports:
        print(f"  - {port}")
    
    # Test each port
    working_ports = []
    for port in arduino_ports:
        if test_port_connection(port):
            working_ports.append(port)
    
    print(f"\n📊 Results:")
    print(f"Working ports: {working_ports}")
    
    if working_ports:
        # Test cvzone with the first working port
        best_port = working_ports[0]
        print(f"\n🎯 Testing cvzone with best port: {best_port}")
        test_cvzone_with_port(best_port)
        
        print(f"\n✅ RECOMMENDED PORT: {best_port}")
        print(f"Use this in your code: SerialObject(digits=3, port='{best_port}')")
    else:
        print("\n❌ No working Arduino ports found!")
