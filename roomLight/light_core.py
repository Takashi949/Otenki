import pigpio
import time

class Light:
    Tunit = 0.00_57
    Tduty = 83

    def __init__(self, PIN) -> None:
        self.PIN = PIN
        self.gpi = pigpio.pi()
        self.gpi.set_mode(PIN, pigpio.OUTPUT)

        self.gpi.set_PWM_frequency(self.PIN, 38*1000)
        self.gpi.set_PWM_dutycycle(self.PIN, 0)

    def LightONOFF(self):
        self.Reader()
        self.Custom()
        self.Data()
        self.DataRev()
        self.One()

        #self.gpi.stop()
        return

    def One(self):
        self.gpi.set_PWM_dutycycle(self.PIN, self.Tduty)
        time.sleep(self.Tunit)
        self.gpi.set_PWM_dutycycle(self.PIN, 0)
        time.sleep(self.Tunit * 3)
        return

    def Zero(self):
        self.gpi.set_PWM_dutycycle(self.PIN, self.Tduty)
        time.sleep(self.Tunit)
        self.gpi.set_PWM_dutycycle(self.PIN, 0)
        time.sleep(self.Tunit)
        return


    def Reader(self):
        #self.gpi.write(self.PIN, pigpio.HIGH)
        #time.sleep(0.009)
        #self.gpi.write(self.PIN, pigpio.LOW)
        #time.sleep(0.0045)
        
        self.gpi.set_PWM_dutycycle(self.PIN, self.Tduty)
        time.sleep(self.Tunit * 16)
        self.gpi.set_PWM_dutycycle(self.PIN, 0)
        time.sleep(self.Tunit * 8)        
        return

    def Custom(self):
        #1010 1110 0100 1000
        self.One()
        self.Zero()
        self.One()
        self.Zero()

        self.One()
        self.One()
        self.One()
        self.Zero()

        self.Zero()
        self.One()
        self.Zero() 
        self.Zero()

        self.One()
        self.Zero()
        self.Zero()
        self.Zero()
        return

    def Data(self):
        #100000000
        self.One()
        self.Zero()   
        self.Zero() 
        self.Zero()
        
        self.Zero() 
        self.Zero()
        self.Zero() 
        self.Zero()
        return

    def DataRev(self):
        #01000000
        self.Zero()
        self.One()
        self.Zero() 
        self.Zero()

        self.Zero() 
        self.Zero()
        self.Zero() 
        self.Zero()
        return

if __name__ == "__main__":
    l = Light(25)
    l.LightONOFF()
