/*
 * Emma Robot Servo Control with PCA9685 PWM Driver
 * Controls 3 servos: Left Arm, Right Arm, and Head
 * Uses PCA9685 PWM servo driver shield for better servo control
 * Receives commands from Python via Serial communication using cvzone
 */

// --- Libraries ---
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <cvzone.h>     // for SerialData (same as your tutorial)

// --- PCA9685 driver on default I2C address 0x40 ---
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

// Choose pulse range for SG-5010 (tune if needed)
#define SERVO_MIN_TICKS 110   // ≈500 µs
#define SERVO_MAX_TICKS 530   // ≈2500 µs
#define SERVO_FREQ_HZ   50    // standard analog servo

// Channels on the PCA9685 for L, R, Head:
const uint8_t CH_LEFT  = 0;
const uint8_t CH_RIGHT = 1;
const uint8_t CH_HEAD  = 2;

// Serial data: 3 values, 3 digits each (same as Python)
SerialData serialData(3, 3);
int valsRec[3];  // [L, R, H] in degrees 0..180

// Servo position variables
int leftPos = 180;   // Left servo position (0-180 degrees)
int rightPos = 0;    // Right servo position (0-180 degrees)
int headPos = 90;    // Head servo position (0-180 degrees)

static uint16_t angleToTicks(int deg) {
  deg = constrain(deg, 0, 180);
  return map(deg, 0, 180, SERVO_MIN_TICKS, SERVO_MAX_TICKS);
}

void setup() {
  // Initialize Serial communication first
  Serial.begin(9600);
  delay(1000);  // Wait for serial to initialize
  
  // Initialize PWM and I2C
  Wire.begin();
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ_HZ);

  // Initialize cvzone serial communication
  serialData.begin();
  
  // Set initial positions
  pwm.setPWM(CH_LEFT,  0, angleToTicks(leftPos));
  pwm.setPWM(CH_RIGHT, 0, angleToTicks(rightPos));
  pwm.setPWM(CH_HEAD,  0, angleToTicks(headPos));
  
  // Wait for servos to reach position
  delay(1000);
  
  Serial.println("Emma Robot Servo Control Ready with PCA9685");
  Serial.println("Baud rate: 9600");
  Serial.println("Channels: P1=Left, P2=Right, P3=Head");
  Serial.println("Initial positions: Left=180, Right=0, Head=90");
}

void loop() {
  // Receive data from Python
  serialData.Get(valsRec);
  
  // Update servo positions if new data received
  if (valsRec[0] != leftPos || valsRec[1] != rightPos || valsRec[2] != headPos) {
    leftPos = valsRec[0];
    rightPos = valsRec[1];
    headPos = valsRec[2];
    
    // Write to channels 1, 2, 3 on the PCA9685 (P1, P2, P3)
    pwm.setPWM(CH_LEFT,  0, angleToTicks(leftPos));
    pwm.setPWM(CH_RIGHT, 0, angleToTicks(rightPos));
    pwm.setPWM(CH_HEAD,  0, angleToTicks(headPos));
    
    // Send confirmation
    Serial.print("Moved to: ");
    Serial.print(leftPos);
    Serial.print(",");
    Serial.print(rightPos);
    Serial.print(",");
    Serial.println(headPos);
  }
  
  // Small delay to prevent overwhelming the system
  delay(10);
}


// //One servo motor code
// #include <Wire.h>
// #include <Adafruit_PWMServoDriver.h>
// #include <cvzone.h>   // for SerialData

// Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

// // pulse range for SG90/standard servos (adjust if needed)
// #define SERVO_MIN 110   // ~500 µs
// #define SERVO_MAX 530   // ~2500 µs

// SerialData serialData(3, 3);  // expecting [L, R, H] in degrees
// int vals[3];

// uint16_t angleToTicks(int deg) {
//   deg = constrain(deg, 0, 180);
//   return map(deg, 0, 180, SERVO_MIN, SERVO_MAX);
// }

// void setup() {
//   Serial.begin(9600);
//   delay(50);
//   Serial.println("READY");

//   Wire.begin();
//   pwm.begin();
//   pwm.setPWMFreq(50);

//   serialData.begin();
// }

// void loop() {
//   // read from Python
//   serialData.Get(vals);
  
//   // Use channels 1, 2, 3 (P1, P2, P3) instead of 0, 1, 2
//   pwm.setPWM(1, 0, angleToTicks(vals[0]));  // P1 = Left servo
//   pwm.setPWM(2, 0, angleToTicks(vals[1]));  // P2 = Right servo  
//   pwm.setPWM(3, 0, angleToTicks(vals[2]));  // P3 = Head servo
  
//   // Debug output
//   Serial.print("Moved to: ");
//   Serial.print(vals[0]);
//   Serial.print(",");
//   Serial.print(vals[1]);
//   Serial.print(",");
//   Serial.println(vals[2]);
// }
// #include <Wire.h>
// #include <Adafruit_PWMServoDriver.h>

// Adafruit_PWMServoDriver pwm(0x40);  // <- force the known-good address

// #define SERVOMIN 110
// #define SERVOMAX 530

// inline int angleToPulse(int ang){
//   if (ang < 0) ang = 0;
//   if (ang > 180) ang = 180;
//   return map(ang, 0, 180, SERVOMIN, SERVOMAX);
// }

// const int SERVO_CH[3] = {0,1,2};

// void moveOne(int ch, int deg){ pwm.setPWM(ch, 0, angleToPulse(deg)); }
// void moveAll(int deg){ for (int i=0;i<3;i++) moveOne(SERVO_CH[i], deg); }

// void setup() {
//   Serial.begin(9600);
//   Wire.begin();
//   pwm.begin();
//   pwm.setPWMFreq(50);
//   delay(10);
//   moveAll(90);  // center so you can see it’s alive
//   Serial.println("Ready. Type in the Serial Monitor and click Send:");
//   Serial.println("  1/2/3 -> that servo to 90°, 0 -> all 0°, 9 -> all 90°, 8 -> all 180°");
// }

// void loop() {
//   if (!Serial.available()) return;
//   char c = Serial.read();
//   if (c=='\r' || c=='\n') return;  // ignore line endings

//   switch (c) {
//     case '1': Serial.println("Servo 1 -> 90°"); moveOne(SERVO_CH[0], 90);  break;
//     case '2': Serial.println("Servo 2 -> 90°"); moveOne(SERVO_CH[1], 90);  break;
//     case '3': Serial.println("Servo 3 -> 90°"); moveOne(SERVO_CH[2], 90);  break;
//     case '0': Serial.println("All -> 0°");     moveAll(0);                 break;
//     case '9': Serial.println("All -> 90°");    moveAll(90);                break;
//     case '8': Serial.println("All -> 180°");   moveAll(180);               break;
//     default:  Serial.print("Unknown key: "); Serial.println(c);
//   }
// }

