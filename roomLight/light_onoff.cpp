#include "io.hpp"
#include <chrono>
#include <thread>
#include <iostream>

#define Tunit 562//562
#define TH 10
#define TL 16
GIO *g;

inline void ichi_T() {
  for (unsigned char i = 0; i < 21; i++) {
    g->digitalHigh();
    std::this_thread::sleep_for(std::chrono::microseconds(TH));
    g->digitalLow();
    std::this_thread::sleep_for(std::chrono::microseconds(TL));
  }
}
inline void w0() {
  ichi_T();
  std::this_thread::sleep_for(std::chrono::microseconds(Tunit));
}

inline void w1() {
  ichi_T();
  std::this_thread::sleep_for(std::chrono::microseconds(Tunit * 3));
}

inline void writeReader() {
  for(unsigned char i = 0; i < 16; i++)ichi_T();
  std::this_thread::sleep_for(std::chrono::microseconds(Tunit * 8));
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
  std::this_thread::sleep_for(std::chrono::microseconds(Tunit * 4));
  w1();
}

int main(){
  g = new GIO(25);
  g->pinOut();

  //g->digitalHigh();

  auto start = std::chrono::system_clock::now();
  for(unsigned int i = 0; i < 1000; i++){
      (i%2?g->digitalHigh():g->digitalLow());
  }
  auto end = std::chrono::system_clock::now();
  std::cout << (end-start).count() << std::endl;

  /*
  auto start = std::chrono::system_clock::now();
  writeReader();
  writeCustom();
  writeData();
  writeRev();
  w1();
  auto end = start + std::chrono::microseconds(108000);
  std::this_thread::sleep_for((end - std::chrono::system_clock::now()));
  writeRepeat();
  */
  return 0;
}
