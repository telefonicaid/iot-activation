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

int first_udp = 0;

DynamicJsonDocument send_UDP_ack(NBUDP Udp, char *packetBuffer){

  StaticJsonDocument<256> jsonBuffer;
  int packetSize = 0;
  
  Serial.print("Send UDP to: ");
  Serial.print(platform);
  Serial.print(":");
  Serial.println(local_Port);
  Serial.println(strlen(packetBuffer));

  Udp.beginPacket(platform, local_Port);
  Udp.write(packetBuffer, strlen(packetBuffer));
  Udp.endPacket();
  Serial.println("Sent packet");  
  
  
  Serial.println("Receiving ack");
  delay(5000);
  packetSize = Udp.parsePacket();
  delay(1000);  
  
  Serial.print("Received packet of size: ");
  Serial.print(packetSize);
  Serial.print(" from: ");
  IPAddress remote = Udp.remoteIP();
    for (int i=0; i < 4; i++) {
        Serial.print(remote[i], DEC);
        if (i < 3) {
            Serial.print(".");
        }
    }
  Serial.print(", port: ");
  Serial.println(Udp.remotePort());
  
  Udp.read(packetBuffer, 255);
  Serial.print ("message received: ");
  Serial.println(packetBuffer);

  DynamicJsonDocument ack_command(256);
  DeserializationError error = deserializeJson(ack_command, packetBuffer);

  return ack_command;

}
