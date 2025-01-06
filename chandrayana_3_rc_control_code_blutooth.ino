#include <SoftwareSerial.h>

// Bluetooth Serial
SoftwareSerial BTSerial(0, 1); // RX, TX
int Speed = 200; // 0 - 255.

// Define motor control pins for Driver 1
const int motor1A = 13; // IN1 for Motor 1
const int motor1B = 12; // IN2 for Motor 1
const int motor2A = A1; // IN3 for Motor 2
const int motor2B = A0; // IN4 for Motor 2
const int enable1A = 11; // ENA for Motor 1
const int enable1B = 10; // ENB for Motor 2

// Define motor control pins for Driver 2
const int motor3A = 7; // IN1 for Motor 3
const int motor3B = 4; // IN2 for Motor 3
const int motor4A = 2; // IN3 for Motor 4
const int motor4B = 8; // IN4 for Motor 4
const int enable2A = 3; // ENA for Motor 3
const int enable2B = 6; // ENB for Motor 4

// Define motor control pins for Driver 3
const int motor5A = A2; // IN1 for Motor 5
const int motor5B = A3; // IN2 for Motor 5
const int motor6A = A4; // IN3 for Motor 6
const int motor6B = A5; // IN4 for Motor 6
const int enable3A = 5; // ENA for Motor 5
const int enable3B = 9; // ENB for Motor 6

void setup() {
  // Start Bluetooth communication
  BTSerial.begin(9600);
  
  // Set motor control pins as outputs
  pinMode(motor1A, OUTPUT);
  pinMode(motor1B, OUTPUT);
  pinMode(motor2A, OUTPUT);
  pinMode(motor2B, OUTPUT);
  pinMode(motor3A, OUTPUT);
  pinMode(motor3B, OUTPUT);
  pinMode(motor4A, OUTPUT);
  pinMode(motor4B, OUTPUT);
  pinMode(motor5A, OUTPUT);
  pinMode(motor5B, OUTPUT);
  pinMode(motor6A, OUTPUT);
  pinMode(motor6B, OUTPUT);
  
  // Set speed control pins as outputs
  pinMode(enable1A, OUTPUT);
  pinMode(enable1B, OUTPUT);
  pinMode(enable2A, OUTPUT);
  pinMode(enable2B, OUTPUT);
  pinMode(enable3A, OUTPUT);
  pinMode(enable3B, OUTPUT);
  
  // Set the initial speed of the motors (0-255)
  updateMotorSpeeds();
}

void loop() {
  if (BTSerial.available()) {
    char command = BTSerial.read(); // Read the command from Bluetooth

    // Control the motors based on the command received
    switch (command) {
      case 'F': // Forward
        moveForward();
        break;
      case 'B': // Backward
        moveBackward();
        break;
      case 'L': // Left
        turnLeft();
        break;
      case 'R': // Right
        turnRight();
        break;
      case 'S': // Stop
        stopMotors();
        break;
      case '0':
        Speed = 40;
        updateMotorSpeeds(); // Update motor speeds
        break;
      case '1':
        Speed = 50;
        updateMotorSpeeds(); // Update motor speeds
        break;
      case '2':
        Speed = 60;
        updateMotorSpeeds(); // Update motor speeds
        break;
      case '3':
        Speed = 80;
        updateMotorSpeeds(); // Update motor speeds
        break;
      case '4':
        Speed = 100;
        updateMotorSpeeds(); // Update motor speeds
        break;
      case '5':
        Speed = 120;
        updateMotorSpeeds(); // Update motor speeds
        break;
      case '6':
        Speed = 140;
        updateMotorSpeeds(); // Update motor speeds
        break;
      case '7':
        Speed = 160;
        updateMotorSpeeds(); // Update motor speeds
        break;
      case '8':
        Speed = 180;
        updateMotorSpeeds(); // Update motor speeds
        break;
      case '9':
        Speed = 190;
        updateMotorSpeeds(); // Update motor speeds
        break;
      case 'q':
        Speed = 200;
        updateMotorSpeeds(); // Update motor speeds
        break;
    }
  }
}

void moveForward() {
  // Set motors to move forward
  digitalWrite(motor1A, HIGH);
  digitalWrite(motor1B, LOW);
  digitalWrite(motor2A, HIGH);
  digitalWrite(motor2B, LOW);
  digitalWrite(motor3A, HIGH);
  digitalWrite(motor3B, LOW);
  digitalWrite(motor4A, HIGH);
  digitalWrite(motor4B, LOW);
  digitalWrite(motor5A, HIGH);
  digitalWrite(motor5B, LOW);
  digitalWrite(motor6A, HIGH);
  digitalWrite(motor6B, LOW);
  
  updateMotorSpeeds(); // Update motor speeds when moving forward
}

void moveBackward() {
  // Set motors to move backward
  digitalWrite(motor1A, LOW);
  digitalWrite(motor1B, HIGH);
  digitalWrite(motor2A, LOW);
  digitalWrite(motor2B, HIGH);
  digitalWrite(motor3A, LOW);
  digitalWrite(motor3B, HIGH);
  digitalWrite(motor4A, LOW);
  digitalWrite(motor4B, HIGH);
  digitalWrite(motor5A, LOW);
  digitalWrite(motor5B, HIGH);
  digitalWrite(motor6A, LOW);
  digitalWrite(motor6B, HIGH);
  
  updateMotorSpeeds(); // Update motor speeds when moving backward
}

void turnLeft() {
  // Set motors to turn left
  digitalWrite(motor1A, HIGH);  // Motor 1 forward
  digitalWrite(motor1B, LOW);
  digitalWrite(motor2A, HIGH);  // Motor 2 forward
  digitalWrite(motor2B, LOW);
  
  digitalWrite(motor3A, HIGH);   // Motor 3 backward
  digitalWrite(motor3B, LOW);
  digitalWrite(motor4A, LOW);   // Motor 4 backward
  digitalWrite(motor4B, HIGH);
  
  digitalWrite(motor5A, LOW);   // Motor 5 backward
  digitalWrite(motor5B, HIGH);
  digitalWrite(motor6A, LOW);   // Motor 6 backward
  digitalWrite(motor6B, HIGH);
  
  updateMotorSpeeds(); // Update motor speeds when turning left
}

void turnRight() {
  // Set motors to turn right
  digitalWrite(motor1A, LOW);
  digitalWrite(motor1B, HIGH); // Motor 1 backward
  digitalWrite(motor2A, LOW);
  digitalWrite(motor2B, HIGH); // Motor 2 forward
  digitalWrite(motor3A, LOW);
  digitalWrite(motor3B, HIGH); // Motor 3 backward
  digitalWrite(motor4A, HIGH);
  digitalWrite(motor4B, LOW); // Motor 4 forward
  digitalWrite(motor5A, HIGH);
  digitalWrite(motor5B, LOW); // Motor 5 backward
  digitalWrite(motor6A, HIGH);
  digitalWrite(motor6B, LOW); // Motor 6 forward
  
  updateMotorSpeeds(); // Update motor speeds when turning right
}

void stopMotors() {
  // Stop all motors
  digitalWrite(motor1A, LOW);
  digitalWrite(motor1B, LOW);
  digitalWrite(motor2A, LOW);
  digitalWrite(motor2B, LOW);
  digitalWrite(motor3A, LOW);
  digitalWrite(motor3B, LOW);
  digitalWrite(motor4A, LOW);
  digitalWrite(motor4B, LOW);
  digitalWrite(motor5A, LOW);
  digitalWrite(motor5B, LOW);
  digitalWrite(motor6A, LOW);
  digitalWrite(motor6B, LOW);
  
  updateMotorSpeeds(); // Update motor speeds when stopping
}
void updateMotorSpeeds() {
  // Update the PWM values for all motors based on the current speed
  analogWrite(enable1A, Speed); // Set speed for Motor 1
  analogWrite(enable1B, Speed); // Set speed for Motor 2
  analogWrite(enable2A, Speed); // Set speed for Motor 3
  analogWrite(enable2B, Speed); // Set speed for Motor 4
  analogWrite(enable3A, Speed); // Set speed for Motor 5
  analogWrite(enable3B, Speed); // Set speed for Motor 6
}
