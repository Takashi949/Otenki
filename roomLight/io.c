#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <errno.h>

#define PERIPHERAL_ADDR 0x3F000000
#define GPIO_ADDR 0x00200000
#define OUT_SET_ADDR 0x001C
#define OUT_CLEAR_ADDR 0x0028
#define HIGH 0b001
#define LOW 0b000

inline void pinOut(int addr, int PIN){
    *(volatile unsigned int*)addr = (HIGH << (PIN * 3)); 
    return ;
}
inline void pinIn(int addr, int PIN){
    *(volatile unsigned int*)addr = LOW << (PIN * 3);
    return;
}

inline void digitalHigh(int addr, int PIN){
    *(volatile unsigned int*)(addr + OUT_SET_ADDR) |= (0b1 << PIN);
    return;
}
inline void digitalLow(int addr, int PIN){
    *(volatile unsigned int*)(addr + OUT_CLEAR_ADDR) |= 0b1 << PIN;
    return;
}
int main(){
    int dm;
    dm = open("/dev/mem", O_RDWR | O_SYNC);
    if(dm < 0){
        //printf("device open error\n");
        perror("err\n");
        return -1;
    }

    unsigned int addr = (unsigned int)mmap(NULL, getpagesize(), PROT_READ | PROT_WRITE, MAP_SHARED, dm, (unsigned int)(PERIPHERAL_ADDR + GPIO_ADDR));
    if(addr == -1){
        printf("mmap failed\n");
        close(dm);
        return -1;
    }

    pinOut(addr, 25);
    digitalHigh(addr, 25);
    close(dm);
    munmap((void*)addr, getpagesize());

    return 0;
}