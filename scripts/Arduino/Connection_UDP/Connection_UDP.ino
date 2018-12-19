////////////////////////////////////////////////////////////////////////////////
// MIT License
//
// Copyright (c) 2018 Telefonica R&D 
//
//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the "Software"), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is
//furnished to do so, subject to the following conditions:
//
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//SOFTWARE.
////////////////////////////////////////////////////////////////////////////////
#include <MKRNB.h>
#include "configuration.h"
#include "my_sensor.h"
#include "send_UDP.h"

NB nbAccess('false');
GPRS gprs;


//variables
my_sensor data;
char data_string[30];
const char PINNUMBER[]=SECRET_PINNUMBER;
const int polling=POLL_TIME*1000;

void setup() {
  
  Serial.begin(9600);
  delay(2000);
  
  Serial.println("START setup");

  Serial.println("Starting Arduino NBIoT Connection.");
  // connection state
  boolean connected = false;

  // After starting the modem with NB.begin()
  // attach the shield to the GPRS network with the APN, login and password
  while (!connected) {
    if ((nbAccess.begin(PINNUMBER) == NB_READY) &&
        (gprs.attachGPRS() == GPRS_READY)) {
      connected = true;
    } else {
      Serial.println("Not connected");
      delay(1000);
    }
  }
  
  nbAccess.lowPowerMode();
  
  Serial.println("END setup");

}

void loop() {
  // put your main code here, to run repeatedly:
    
  Serial.println("measuring...");
  data.measurement();
  Serial.print("- voltage: ");
  Serial.println(data.get_voltage());
  Serial.print("- amperage: "); 
  Serial.println(data.get_amperage());

  Serial.println("Sending... ");  
    
  
  send_data_UDP(data.get_voltage(),data.get_amperage()); 
  
  
  delay(polling);
}
