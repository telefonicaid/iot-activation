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
#include <Modem.h>

int apply(){  
  MODEM.send("AT+CFUN=15");
  MODEM.waitForResponse(5000);
  delay(5000);

  do {
    delay(1000);
    MODEM.noop();
  } while (MODEM.waitForResponse(1000) != 1);
   
  return 0;
}

int setup_SaraR410M_movistar(){

  String response;
  MODEM.begin();

  while (!MODEM.noop());


  //// Disconnecting from network
  //MODEM.sendf("AT+COPS=2"); 
  MODEM.sendf("AT+CFUN=0");
  MODEM.waitForResponse(2000);
  
  

  //// Select Radio Access Technology (RAT)
  //// uncomment only 1 of the 4 options
  
  //// LTE only
  //MODEM.sendf("AT+URAT=7");
  //// NB-IoT only
  MODEM.sendf("AT+URAT=8");
  //// LTE-M preferred, NB-IoT as failover
  //MODEM.sendf("AT+URAT=7,8"); 
  //// NB-IoT preferred, LTE-M as failover
  //MODEM.sendf("AT+URAT=8,7");
  ////wait response
  MODEM.waitForResponse(2000, &response);
  
  //// Select Band bitmask 
  //// configure both masks if necessary (LTE-M and NB-IoT )
  
  //// configure bitmask for LTE-M (Band-20)
  MODEM.sendf("AT+UBANDMASK=0,524288");
  MODEM.waitForResponse(2000, &response);
  //// configure bitmask for NB-IoT (Band-20)
  MODEM.sendf("AT+UBANDMASK=1,524288");
  MODEM.waitForResponse(2000, &response);  

  ////configure the default values for Mobile Network Operators
  MODEM.sendf("AT+UMNOPROF=0");
  MODEM.waitForResponse(2000, &response);

  ////configure the APN if you know it
  //MODEM.sendf("AT+CGDCONT=1,\"IP\",\"sm2m-apple.movistar.es\"");  
  MODEM.waitForResponse(2000, &response);  
  
  ////// Configures the Extended Discontinuous Reception (eDRX).   
  MODEM.sendf("AT+CEDRXS=0");
  //// in LTE-M
  // MODEM.sendf("AT+CEDRXS=2,4\"0010\"");
  //// or in NB-Iot
  // MODEM.sendf("AT+CEDRXS=2,5\"0010\"");    
  MODEM.waitForResponse(2000, &response);
  
  ////// Configures the Power Saving Mode (PSM).   
  MODEM.sendf("AT+CPSMS=0");  
  //MODEM.sendf("AT+CPSMS=1,\"00100001\",\"00100101\"");  
  MODEM.waitForResponse(2000, &response);    
    
  //// Applying changes and saving configuration
  apply();
  
	return 0;  
}
