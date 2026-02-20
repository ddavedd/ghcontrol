/*
  Analog input, analog output, serial output

  Reads an analog input pin, maps the result to a range from 0 to 255 and uses
  the result to set the pulse width modulation (PWM) of an output pin.
  Also prints the results to the Serial Monitor.

  The circuit:
  - potentiometer connected to analog pin 0.
    Center pin of the potentiometer goes to the analog pin.
    side pins of the potentiometer go to +5V and ground
  - LED connected from digital pin 9 to ground through 220 ohm resistor

  created 29 Dec. 2008
  modified 9 Apr 2012
  by Tom Igoe

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogInOutSerial
*/

// These constants won't change. They're used to give names to the pins used:
const int analogIn0 = A0;  // Analog input pin that the potentiometer is attached to
const int analogIn1 = A1;
const int analogIn2 = A2;
const int analogIn3 = A3;
const int analogIn4 = A4;
const int analogIn5 = A5;

unsigned long seconds_since_start = 0;
int sensorValue = 0;        // value read from the pot
const byte interruptPin = 2;
volatile unsigned long water_pulses = 0; 

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(interruptPin), count_pulse, RISING);
}

void count_pulse() {
  water_pulses += 1;
}
void loop() {
  String analog_string = "";
  analog_string += "D2," + String(seconds_since_start) + "," + String(water_pulses) + "\n";
  // read the analog in value:
  analog_string += "A0," + String(seconds_since_start) + "," + String(analogRead(analogIn0)) +"\n";
  analog_string += "A1," + String(seconds_since_start) + "," + String(analogRead(analogIn1)) +"\n";
  analog_string += "A2," + String(seconds_since_start) + "," + String(analogRead(analogIn2)) +"\n";
  analog_string += "A3," + String(seconds_since_start) + "," + String(analogRead(analogIn3)) +"\n";
  analog_string += "A4," + String(seconds_since_start) + "," + String(analogRead(analogIn4)) +"\n";
  analog_string += "A5," + String(seconds_since_start) + "," + String(analogRead(analogIn5)) +"\n";
  
  // print the results to the Serial Monitor:
  Serial.print(analog_string);
  seconds_since_start++;
  // wait 2 milliseconds before the next loop for the analog-to-digital
  // converter to settle after the last reading:
  delay(1000);
}
