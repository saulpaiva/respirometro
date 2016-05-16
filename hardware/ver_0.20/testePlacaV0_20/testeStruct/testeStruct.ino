#include"binaryCommunication.h"
/*
  ReadAnalogVoltage
  Reads an analog input on pin 0, converts it to voltage, and prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
 
 This example code is in the public domain.
 */
struct Data{
  short int x1; 
  short int x2;
  float x3;
}data;


// BinCommunication comm = new BinCommunication();
BinCommunication comm(&data, sizeof(data));
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  comm.begin(9600);
  data.x1 = 0;
  data.x2 = 0;
  data.x3 = 0;
  byte b = 10;
  Serial.write(b);
  Serial.write(0);
}

// the loop routine runs over and over again forever:
void loop() {
  data.x1 ++;
  data.x2 += 2;
  data.x3 += 0.1;
  comm.send();
  delay(100);
}
