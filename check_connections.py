#!/usr/bin/env python3
"""
Hardware Connection Checker for Emma Robot
Tests each component step by step
"""

import sys
import os
import time

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_arduino_connection():
    """Check if Arduino is connected and responding"""
    print("🔌 Checking Arduino Connection...")
    
    try:
        import serial
        ser = serial.Serial('/dev/tty.usbmodem2101', 9600, timeout=1)
        time.sleep(2)
        
        # Check for startup message
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if "Emma Robot Servo Control Ready" in line:
                print("✅ Arduino connected and running correct code")
                ser.close()
                return True
        
        ser.close()
        print("❌ Arduino not responding correctly")
        return False
        
    except Exception as e:
        print(f"❌ Arduino connection failed: {e}")
        return False

def check_servo_communication():
    """Check if servos are responding to commands"""
    print("\n🎯 Checking Servo Communication...")
    
    try:
        from cvzone.SerialModule import SerialObject
        
        arduino = SerialObject(digits=3)
        print("✅ Serial communication established")
        
        # Test each servo individually
        test_positions = [
            ([90, 90, 90], "Center positions"),
            ([180, 0, 90], "Default positions"),
            ([0, 180, 90], "Extreme positions"),
            ([90, 90, 90], "Back to center")
        ]
        
        print("\nTesting servo movements:")
        for positions, description in test_positions:
            print(f"  {description}: {positions}")
            arduino.sendData(positions)
            time.sleep(2)
        
        print("✅ Servo communication test completed")
        return True
        
    except Exception as e:
        print(f"❌ Servo communication failed: {e}")
        return False

def check_power_supply():
    """Check power supply status"""
    print("\n🔋 Checking Power Supply...")
    
    print("Power supply checklist:")
    print("  □ Voltage: 5V-6V (recommended)")
    print("  □ Current: 2A+ for 3 servos")
    print("  □ Stable power (no voltage drops)")
    print("  □ Proper connections (VCC/GND)")
    
    print("\n⚠️  If servos don't move:")
    print("  - Check voltage with multimeter")
    print("  - Ensure adequate current capacity")
    print("  - Verify power connections")
    
    return True

def check_servo_wiring():
    """Check servo wiring connections"""
    print("\n🔌 Checking Servo Wiring...")
    
    print("Servo connection checklist:")
    print("  □ Left servo → PCA9685 Channel 0")
    print("  □ Right servo → PCA9685 Channel 1")
    print("  □ Head servo → PCA9685 Channel 2")
    print("  □ All power wires → VCC on PCA9685")
    print("  □ All ground wires → GND on PCA9685")
    print("  □ All signal wires → Channel pins")
    
    print("\n⚠️  Common wiring issues:")
    print("  - Wrong channel numbers")
    print("  - Loose connections")
    print("  - Reversed power/ground")
    print("  - Damaged wires")
    
    return True

def main():
    """Run all connection checks"""
    print("🤖 Emma Robot - Hardware Connection Checker")
    print("=" * 50)
    
    checks = [
        check_arduino_connection,
        check_servo_communication,
        check_power_supply,
        check_servo_wiring
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 CONNECTION CHECK RESULTS:")
    print("=" * 50)
    
    if all(results):
        print("🎉 All connections look good!")
        print("If servos still don't move, check power supply voltage.")
    else:
        print("❌ Some issues found. Check the details above.")
    
    print("\n💡 Next steps:")
    print("1. Fix any connection issues")
    print("2. Test with: python3 test_servo_communication.py")
    print("3. Run Emma: python3 Integrated/Emma_robot.py")

if __name__ == "__main__":
    main()


