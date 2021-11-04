#coding:utf-8
import firebase_admin
from firebase_admin import db
import datetime
import pytz
import subprocess
#import FAN

import RPi.GPIO as GPIO
import dht11
import time
import atexit

def cleanup():
    lis.close()
    exit()

def dht():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    dhtrst = dht11.DHT11(23).read()
    while dhtrst.temperature == 0 and dhtrst.humidity == 0:
        time.sleep(5)
        dhtrst = dht11.DHT11(23).read()
    return dhtrst 

def listener(event):
    #print(event.path)  # relative to the reference, it seems
    #print(event.data)  # new data at /reference/event.path. None if deleted
    #コマンドは全部小文字にしましょ
    if str(event.data) == "exit":
        db.reference("CmdResult").set({"msg":"exit", "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()})
        cleanup()
    elif str(event.data) == "temp":
        temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        db.reference("CmdResult").set({"msg":temp[5:-3], "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()})
    elif str(event.data) == "update":
        subprocess.check_output(["python3", "/home/pi/npy.py"]).decode("utf-8")
    elif str(event.data) == "ping":
        db.reference("CmdResult").set({"msg":"pong", "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()})
        """     elif str(event.data) == "fan":
        ff.ChangeState()
        fs.ChangeState()
        db.reference("Fan").set({"fan1":ff.getDuty(), "fan2":fs.getDuty(),  "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()})
        db.reference("CmdResult").set({"msg":"success", "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()}) 
        """
    elif str(event.data) == "shutdown":
        db.reference("CmdResult").set({"msg":"shutdown", "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()})
        lis.close()
        subprocess.check_output(["sudo", "shutdown", "-h","now"]).decode("utf-8")
    elif str(event.data) == "picture":
        db.reference("CmdResult").set({"msg":"picture", "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()})
    elif str(event.data) == "dhttemp":
        db.reference("CmdResult").set({"msg":dht().temperature, "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()})
    elif str(event.data) == "dhthum":
        db.reference("CmdResult").set({"msg":dht().humidity, "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()})
    elif str(event.data).startswith("fan"):
        lk = str(event.data)
        kk = lk[3:]
        
        if kk.startswith("1"):
            db.reference("Fan").child("fan1").set(int(kk[1:]))
            db.reference("Fan").child("date").set(datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat())
        elif kk.startswith("2"):
            db.reference("Fan").child("fan2").set(int(kk[1:]))
            db.reference("Fan").child("date").set(datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat())
        db.reference("CmdResult").set({"msg":"success", "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()})
    db.reference("Cmd").set({"cmd":"f"})

firebase_admin.initialize_app()

lis = db.reference("Cmd").listen(listener)
atexit.register(cleanup)
