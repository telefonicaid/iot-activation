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
#ifndef my_sensor_h
#define my_sensor_h

class my_sensor {
  private:
  	int _voltage;
  	int _amperage;
    
  
  public:
    //Constructor
    my_sensor();
    //set function
    void set_voltage();  
    void set_amperage();  
    void measurement();
    //get function  
    int get_voltage();  
    int get_amperage();   
    
} ;

#endif
