/*
  Read analog pins and a single interrupt pin for Arduino uno
  Can read 1 more interrupt pin on pin3 if necessary
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
  String analog_string = String(seconds_since_start) + ",\t";
  analog_string += "D2," + String(water_pulses) + ",\t";
  analog_string += "A0," + String(analogRead(analogIn0)) +",\t";
  analog_string += "A1," + String(analogRead(analogIn1)) +",\t";
  analog_string += "A2," + String(analogRead(analogIn2)) +",\t";
  analog_string += "A3," + String(analogRead(analogIn3)) +",\t";
  analog_string += "A4," + String(analogRead(analogIn4)) +",\t";
  analog_string += "A5," + String(analogRead(analogIn5)) +",\t\n";
  
  // print the results to the Serial Monitor:
  Serial.print(analog_string);
  seconds_since_start++;
  // wait 2 milliseconds before the next loop for the analog-to-digital
  // converter to settle after the last reading:
  delay(1000);
}
