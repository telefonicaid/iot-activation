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
#include <ArduinoJson.h>
#include "configuration.h"
#include "my_sensor.h"
#include "send_UDP.h"
#include "device.h"
#include "setup_SaraR410M_movistar.h"

// Const
const int PACKET_BUFFER_SIZE = 255;

// Variables
NB nbAccess(1);
GPRS gprs;
NBUDP Udp;
my_sensor data;

char packetBuffer[PACKET_BUFFER_SIZE]; //buffer to send packets
//char data_string[30];
const char PINNUMBER[]=SECRET_PINNUMBER;
const int polling=POLL_TIME*1000;


void setup() {

  // enable the POW_ON pin
  pinMode(SARA_PWR_ON, OUTPUT);
  digitalWrite(SARA_PWR_ON, HIGH);
  // reset the ublox module
  pinMode(SARA_RESETN, OUTPUT);
  digitalWrite(SARA_RESETN, HIGH);
  delay(100);
  digitalWrite(SARA_RESETN, LOW);
  

  
  Serial.begin(9600);
  delay(2000);
  Serial.println("11111111111111111111111111111111111111111");
  setup_SaraR410M_movistar();
  
  Serial.println("START setup");

  Serial.println("Starting Arduino NBIoT/LTE-M Connection.");
  // connection state
  boolean connected = false;

  // After starting the modem with NB.begin()
  // attach the shield to the GPRS network with the APN, login and password
  while (!connected) {
    Serial.println("Try Connection.");
    delay(2000);
    if ((nbAccess.begin(PINNUMBER) == NB_READY) &&
        (gprs.attachGPRS() == GPRS_READY)) {
      connected = true;
    } else {
      Serial.println("Not connected");      
    }
    
  }
  
  Udp.begin(local_Port);

  device_setup();
  
  Serial.println("END setup");

}

void loop() {
  // put your main code here, to run repeatedly:
    
  Serial.println("measuring...");
  data.measurement();
  Serial.print("- voltage: ");
  Serial.println(data.get_voltage());
  Serial.print("- amperage: "); 
  Serial.println();  
      
  Serial.println("Formating...");
  memset(packetBuffer, 0x00, PACKET_BUFFER_SIZE);
  sprintf(packetBuffer,"{\"v\":%d,\"a\":%d}",data.get_voltage(),data.get_amperage());
  Serial.println(packetBuffer);

  Serial.println("Sending data to UDP ... ");      
  JsonObject& ack_command = send_UDP_ack(Udp,packetBuffer); 

  if (ack_command["code"] == 200){
    Serial.print("command: ");
    char msg = ack_command["msg"];
    Serial.println(msg); 
    char status_device = device_task(msg);
  }
  
  
  Serial.print("waiting for "); 
  Serial.print(polling/1000); 
  Serial.println(" seconds ... "); 
  delay(polling);
}
