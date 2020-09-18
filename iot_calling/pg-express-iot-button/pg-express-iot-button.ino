#include <Adafruit_CircuitPlayground.h>
 
void setup() {
  // Initialize the circuit playground
  Serial.begin(9600);
  CircuitPlayground.begin();
  
}
 
void loop() {
  // If the left button is pressed....
  if (CircuitPlayground.leftButton()) {
      CircuitPlayground.redLED(HIGH);  // LED on
      Serial.println("1");
  } else {
      CircuitPlayground.redLED(LOW);   // LED off
  }
}
