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
const int PACKET_SIZE = 256; // NTP time stamp is in the first 48 bytes of the message

//unsigned int localPort = LOCAL_PORT;  // local port to listen for UDP packets
//IPAddress platform(IP_ADDRESS);       // Servidor
unsigned int localPort = LOCAL_PORT;      // local port to listen for UDP packets

String ip = IP_ADDRESS;
String ip_0 = getValue(ip,'.', 0);
String ip_1 = getValue(ip,'.', 1);
String ip_2 = getValue(ip,'.', 2);
String ip_3 = getValue(ip,'.', 3);
IPAddress platform(ip_0.toInt(),ip_1.toInt(),ip_2.toInt(),ip_3.toInt()); // Servidor

NBUDP Udp;
NBUDP Udp2;

// function
int send_data_UDP(int data1, int data2){

  char packetBuffer[PACKET_SIZE]; //buffer to send packets
  char packetBuffer_ack[PACKET_SIZE]; //buffer to receive packetss
  
  Serial.println("Formating...");
  memset(packetBuffer, 0x00, PACKET_SIZE);
  sprintf(packetBuffer,"{\"v\":%d,\"a\":%d}",data1,data2);
  Serial.println(packetBuffer);
  
  Serial.println("Sending UDP...");
  Serial.print("- packet length: ");
  Serial.println(strlen(packetBuffer));

  Serial.println("Connecting to server...");
  Udp.begin(localPort);
  Udp2.begin(localPort);
  bool ack = false;
  int packetSize = 0;
   
  Serial.println("Sending packet...");
  Serial.print(platform);
  Serial.print(":");
  Serial.println(localPort);
  
  Udp.beginPacket(platform, localPort);
  Udp.write(packetBuffer, strlen(packetBuffer));
  Udp.endPacket();
  Serial.println("Sent packet");
  
  ///////////////////////////////////////////////////////////////////////////////////
 
  Serial.println("Receiving ack...");
  while (!ack){
      packetSize = Udp2.parsePacket();
      Serial.println("Waiting ack...");
      if (packetSize){
          ack = true;
          Serial.print("Received packet of size: ");
          Serial.println(packetSize);
      }
    
  }    
    // read the packet into packetBufffer
    Udp2.read(packetBuffer_ack , PACKET_SIZE);
    Serial.print("Contents:");
    Serial.println(packetBuffer_ack);
  
   
}
