#pragma once
class GIO{
    unsigned int dm;
    unsigned int addr;
    unsigned char pin;
public:
    GIO(unsigned char PIN);
    ~GIO();
    void digitalHigh();
    void digitalLow();
    void pinOut();
    void pinIn();
};