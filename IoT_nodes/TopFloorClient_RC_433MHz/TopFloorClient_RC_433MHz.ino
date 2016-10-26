//
// An Arduino sketch for an IoT node that broadcasts sensor values via 
// 433 MHz radio signals
// The RCSwitch library is used for the transmissions
// The Narcopleptic library is used for power save during delay
// Sensor values are fetched from an BPM180/085 sensor via i2C
// 

#include <Wire.h>
#include <Adafruit_BMP085.h>
#include "RCSwitch.h"
#include <Narcoleptic.h>

#define CLIENT_NAME "TopFloorClient"
#define TX_PIN 10                     // PWM output pin to use for transmission

//
// Sensor setup
// The BMP085 module measure ait pressure and temperature and operates via i2C
//
Adafruit_BMP085 bmp; // pin 4, SDA (data), pin 5, SDC (clock)

//
// Data transmission setup
//
#define TOPFLOOR_TEMP_ID    1
#define BMP_PRESSURE_ID     2
RCSwitch transmitter = RCSwitch();

void setup() 
{
  Serial.begin(9600);
  
  bmp.begin();

  transmitter.enableTransmit(TX_PIN); 
  transmitter.setRepeatTransmit(25);
}

unsigned long seqNum=0;
void loop() 
{
  float temp = bmp.readTemperature();
  Serial.print("Temperature = ");
  Serial.print(temp);
  Serial.println(" *C");

  unsigned int encodedFloat = EncodeFloatToTwoBytes(temp);
  unsigned long dataToSend = Code32BitsToSend(TOPFLOOR_TEMP_ID,seqNum,encodedFloat);
  TransmitWithRepeat(dataToSend);

  float pressure = bmp.readPressure();
  unsigned int pressureAsInt = pressure/100;
  Serial.print("Pressure = ");
  Serial.print(pressureAsInt);
  Serial.println(" hPa");
  dataToSend = Code32BitsToSend(BMP_PRESSURE_ID,seqNum,pressureAsInt);
  TransmitWithRepeat(dataToSend);

  for (int i=0; i< 100; i++)
  {
    // Max narcoleptic delay is 8s
    Narcoleptic.delay(8000);
  }

  seqNum++;
  if (seqNum > 15)
  {
    seqNum = 0;
  } 
}


unsigned long Code32BitsToSend(int measurementTypeID, unsigned long seq, unsigned long data)
{
    unsigned long checkSum = measurementTypeID + seq + data;
    unsigned long byte3 = ((0x0F & measurementTypeID) << 4) + (0x0F & seq);
    unsigned long byte2_and_byte_1 = 0xFFFF & data;
    unsigned long byte0 = 0xFF & checkSum;
    unsigned long dataToSend = (byte3 << 24) + (byte2_and_byte_1 << 8) + byte0;

    return dataToSend;
}

// Encode a float as two bytes by multiplying with 100
// and reserving the highest bit as a sign flag
// Values that can be encoded correctly are between -327,67 and +327,67
unsigned int EncodeFloatToTwoBytes(float floatValue)
{
  bool sign = false;
  
  if (floatValue < 0) 
    sign=true;  
      
  int integer = (100*fabs(floatValue));
  unsigned int word = integer & 0XFFFF;
  
  if (sign)
    word |= 1 << 15;

  return word;
}

void TransmitWithRepeat(unsigned long dataToSend)
{
    transmitter.send(dataToSend, 32);
    Narcoleptic.delay(2000);
    transmitter.send(dataToSend, 32);
    Narcoleptic.delay(2000);
}

