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
#include <ArduinoJson.h>

JsonObject& send_UDP_ack(NBUDP Udp, char *packetBuffer){

  //DynamicJsonDocument jsonBuffer;
  //DynamicJsonBuffer jsonBuffer;  
  StaticJsonBuffer<200> jsonBuffer;
  int packetSize = 0;

  Serial.println("Sending UDP...");
  Serial.print("- packet length: ");
  Serial.println(strlen(packetBuffer));

  Serial.println("Sending packet...");
  Serial.print(platform);
  Serial.print(":");
  Serial.println(local_Port);

  Udp.beginPacket(platform, local_Port);
  Udp.write(packetBuffer, strlen(packetBuffer));
  Udp.endPacket();
  Serial.println("Sent packet");  

  Serial.println("Receiving ack...");

  bool ack = false;
  int cont = 5;

  delay(100);  

  while (cont > 0 and (!ack)){    

      packetSize = Udp.parsePacket();
      if (packetSize) {

        Serial.print("Received packet of size: ");
        Serial.println(packetSize);
        Serial.print("From ");
        IPAddress remote = Udp.remoteIP();
        for (int i=0; i < 4; i++) {
            Serial.print(remote[i], DEC);
            if (i < 3) {
                Serial.print(".");
            }
        }
        Serial.print(", port ");
        Serial.println(Udp.remotePort());

        // read the packet into packetBufffer
        Udp.read(packetBuffer, 255);
        Serial.print ("Contents: ");
        Serial.println(packetBuffer);
        
        //JsonObject& ack_command = jsonBuffer.parseObject(packetBuffer);
        JsonObject& ack_command = jsonBuffer.parseObject(packetBuffer);  
        ack = true;
        Serial.println("Completed Reading");
        return ack_command;
    } 
    Serial.print("Waiting ack ");
    Serial.println(cont);
    delay(1000);
    cont = cont - 1;
  }

  JsonObject& ack_default = jsonBuffer.createObject();
  ack_default["code"] = 0;
  return ack_default;

}
