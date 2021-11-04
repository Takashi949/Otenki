#coding:utf-8
import firebase_admin
from firebase_admin import firestore
import datetime
import pytz
import subprocess
#import FAN

import RPi.GPIO as GPIO
import dht11
import time
import atexit

def cleanup():
    lis.unsubscribe()
    exit()

def dht():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    dhtrst = dht11.DHT11(23).read()
    while dhtrst.temperature == 0 and dhtrst.humidity == 0:
        time.sleep(5)
        dhtrst = dht11.DHT11(23).read()
    return dhtrst 

def listener(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(doc.to_dict()[u'cmd'])
    db.collection(u'Cmd').document(u'cmd').set({"cmd":"f"})
    #コマンドは全部小文字にしましょ
    if doc.to_dict()[u'cmd'] == "exit":
        db.collection(u'CmdResult').document(u'cmdResult').set({"msg":"exit", "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo"))})
        cleanup()
    elif doc.to_dict()[u'cmd'] == "temp":
        temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        db.collection(u'CmdResult').document(u'cmdResult').set({"msg":temp[5:-3], "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo"))})
    elif doc.to_dict()[u'cmd'] == "update":
        subprocess.check_output(["python3", "/home/pi/Otenki/firestore/npy.py"]).decode("utf-8")
    elif doc.to_dict()[u'cmd'] == "ping":
        db.collection(u'CmdResult').document(u'cmdResult').set({"msg":"pong", "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo"))})
    elif doc.to_dict()[u'cmd'] == "dhttemp":
        db.collection(u'CmdResult').document(u'cmdResult').set({"msg":dht().temperature, "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo"))})
    elif doc.to_dict()[u'cmd'] == "dhthum":
        db.collection(u'CmdResult').document(u'cmdResult').set({"msg":dht().humidity, "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo"))})
    elif doc.to_dict()[u'cmd'].startswith("fan"):
        lk = doc.to_dict()[u'cmd']
        kk = lk[3:]
        
        if kk.startswith("1"):
            db.reference("Fan").child("fan1").set(int(kk[1:]))
            db.reference("Fan").child("date").set(datetime.datetime.now(pytz.timezone("Asia/Tokyo")))
        elif kk.startswith("2"):
            db.reference("Fan").child("fan2").set(int(kk[1:]))
            db.reference("Fan").child("date").set(datetime.datetime.now(pytz.timezone("Asia/Tokyo")))
        db.collection(u'CmdResult').document(u'cmdResult').set({"msg":"success", "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo"))})
    elif doc.to_dict()[u'cmd'] == "lightonoff":
        subprocess.call(["/home/pi/Otenki/roomLight/Light"])
        db.collection(u'CmdResult').document(u'cmdResult').set({"msg":"lf", "date":datetime.datetime.now(pytz.timezone("Asia/Tokyo"))})


firebase_admin.initialize_app()

db = firestore.client()
lis = db.collection(u'Cmd').document(u'cmd').on_snapshot(listener)
atexit.register(cleanup)

while True:
    pass
