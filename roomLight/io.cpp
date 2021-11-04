#include <iostream>
#include <fstream>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <errno.h>
#include "io.hpp"

#define PERIPHERAL_ADDR 0x3F000000
#define GPIO_ADDR 0x00200000
#define OUT_SET_ADDR 0x001C
#define OUT_CLEAR_ADDR 0x0028
#define HIGH 0b001
#define LOW 0b000


GIO::GIO(unsigned char PIN){
    pin = PIN;

    dm = open("/dev/mem", O_RDWR | O_SYNC);
    if(dm < 0){
        perror("err");
    }
    std::cout << dm << std::endl;
    addr = (unsigned int)mmap(NULL, getpagesize(), PROT_READ | PROT_WRITE, MAP_SHARED, dm, (unsigned int)(PERIPHERAL_ADDR + GPIO_ADDR));
    if(addr == -1){
        perror("mmap failed ");
        close(dm);
    }
    std::cout << addr << std::endl;
    
}
GIO::~GIO(){
    close(dm);
    munmap((void*)addr, getpagesize());
}

void GIO::pinOut(){
    *(volatile unsigned int*)addr = (HIGH << (pin * 3)); 
    return ;
}
void GIO::pinIn(){
    *(volatile unsigned int*)addr = (LOW << (pin * 3));
    return;
}

void GIO::digitalHigh(){
    *(volatile unsigned int*)(addr + OUT_SET_ADDR) |= (0b1 << pin);
    return;
}
void GIO::digitalLow(){
    *(volatile unsigned int*)(addr + OUT_CLEAR_ADDR) |= (0b1 << pin);
    return;
}