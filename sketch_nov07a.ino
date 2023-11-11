#include <Servo.h>

Servo servo; // Create a servo object to control a servo motor

void setup() {
  servo.attach(9); // Attaches the servo on pin 9
}

void loop() {
  for (int angle = 0; angle <= 180; angle += 1) { // Sweep from 0 to 180 degrees
    servo.write(angle); // Set the servo position
    delay(15); // Delay for smooth movement (you can adjust this value)
  }

  delay(1000); // Pause at 180 degrees for 1 second
  
  for (int angle = 180; angle >= 0; angle -= 1) { // Sweep from 180 to 0 degrees
    servo.write(angle); // Set the servo position
    delay(15); // Delay for smooth movement (you can adjust this value)
  }

  delay(1000); // Pause at 0 degrees for 1 second
}
