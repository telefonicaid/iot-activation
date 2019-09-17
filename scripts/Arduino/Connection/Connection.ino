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
// libraries
#include <MKRNB.h>
#include "setup_SaraR410M_telefonica.h"

// initialize the library instance
NBScanner scannerNetworks;
NB nbAccess; // include a 'true' parameter to enable debugging
GPRS gprs;

// data
const char PINNUMBER[] = ""; //enter your pin number
String IMEI = "";
boolean connected = false;

/**
  start modem test (reset and check response)
  @return IMEI number
*/
String test_modem() {
  String n_imei = "";
  NBModem modemTest;

  Serial.println("- Starting modem test...");
  if (modemTest.begin()) {
    Serial.println("- Modem is connected");
  } else {
    Serial.println("- ERROR, no modem answer.");
  }

  Serial.println("- Checking IMEI...");
  n_imei = modemTest.getIMEI();
  delay(5000);

  // check IMEI response
  if (n_imei != NULL) {
    Serial.println("- Modem is functioning properly");
    // reset modem to check booting:
    Serial.println("- Resetting modem...");
    modemTest.begin();
    // get and check IMEI one more time
    if (modemTest.getIMEI() != NULL) {
      Serial.println("- Modem is functioning properly");
    } else {
      Serial.println("- Error: Modem failed after reset");
    }
  } else {
    Serial.println("- Error: Could not get IMEI");
  }

  return n_imei;
}

/**
  setup board  
  @return void
*/
void setup() {
  Serial.begin(9600);
  while (!Serial) {;}
  
  Serial.println("START setup");
  //setup modem Sara R410M
  setup_SaraR410M_telefonica();
  
  Serial.println("Testing Modem:");
  IMEI = test_modem();
  Serial.println("Modem's IMEI: " + IMEI);
  
  while (!connected) {
    Serial.println("Try Connecting....");
    if ((nbAccess.begin(PINNUMBER) == NB_READY) && (gprs.attachGPRS() == GPRS_READY) ) {
      connected = true;
      Serial.println("Connected");
    } else {
      Serial.println("Not connected");
      delay(1000);
    }
  }

  Serial.println("END setup");

}

/**
  main loop  
*/
void loop() {
  
  // put your main code here, to run repeatedly:
  if (nbAccess.isAccessAlive() == 1){
     Serial.print("Connected:");
     Serial.println(nbAccess.getLocalTime());
     
  }else{
    Serial.println("Not connected");
  }
  delay(5000);
}
