#include "light_core.hpp"
#include <wiringPi.h>
#include <stdlib.h>

inline void ichi_T() {
  for (unsigned char i = 0; i < 21; i++) {
    digitalWrite(PIN, HIGH);
    delayMicroseconds(HZ);
    digitalWrite(PIN, LOW);
    delayMicroseconds(HL);
  }
}
inline void w0() {
  ichi_T();
  delayMicroseconds(Tunit);
}

inline void w1() {
  ichi_T();
  delayMicroseconds(Tunit * 3);
}

inline void writeReader() {
  for(unsigned char i = 0; i < 16; i++)ichi_T();
  delayMicroseconds(Tunit * 8);
}
inline void writeCustom() {
  //01010001
  w1();
  w0();
  w1();
  w0();

  w1();
  w1();
  w1();
  w0();

  //10110111
  w0();
  w1();
  w0();
  w0();

  w1();
  w0();
  w0();
  w0();
}
inline void writeData() {
  //01111111
  w1();
  w0();
  w0();
  w0();

  w0();
  w0();
  w0();
  w0();
}
inline void writeRev() {
  //10111111
  w0();
  w1();
  w0();
  w0();

  w0();
  w0();
  w0();
  w0();
}

inline void writeRepeat(){
  for(unsigned char i = 0; i < 16; i++)ichi_T();
  delayMicroseconds(Tunit * 4);
  w1();
}
void LightONOFF(){
  unsigned int start = micros();
  writeReader();
  writeCustom();
  writeData();
  writeRev();
  w1();
  delayMicroseconds(108000 - start);


}

int main(){
  wiringPiSetupGpio();
  pinMode(PIN, OUTPUT);
  LightONOFF();
  return 0;
}