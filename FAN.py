# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import socket

class FAN:
   def __init__(self, PINNUM):
      self.PIN = PINNUM
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      GPIO.setup(self.PIN, GPIO.OUT)
      self.freq = 30 # Hz (PWM のパルスを一秒間に 50 個生成)
      self.duty = 40.0 # デューティー比 0.0 で出力開始 (パルス内に占める HIGH 状態の時間が 0.0 %)
      self.pwm = GPIO.PWM(self.PIN, self.freq)
      self.pwm.start(self.duty)

   def STOP(self):
       #print("stop")
       self.duty = 0.0
       self.pwm.ChangeDutyCycle(self.duty)
   
   def Change(self, du):
       self.duty = du
       self.pwm.ChangeDutyCycle(self.duty)

   def ChangeState(self):
       if(0.0 <= self.duty < 50.0):
           self.pwm.ChangeDutyCycle(100)
           time.sleep(1)
           self.duty = 50.0
       elif(50.0 <= self.duty < 100.0):
           self.duty = 100.0
       else:
           self.duty = 0.0
       self.pwm.ChangeDutyCycle(self.duty)

   def getDuty(self):
       return self.duty

   def __del__(self):
       self.pwm.stop()
       GPIO.cleanup()

if __name__ == '__main__':
   ff = FAN(17)
   fs = FAN(27)
   HOST='localhost'
   PORT=60000
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: 
      sock.bind((HOST, PORT))
      sock.listen(1)
      while True:
         conn, addr = sock.accept()
         with conn:
            rec = conn.recv(1024).decode('UTF-8')
            print(rec)
            if(rec.startswith("1")):
                ff.Change(int(rec[1:]))
            elif(rec.startswith("2")):
                fs.Change(int(rec[1:]))
