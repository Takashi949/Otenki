import RPi.GPIO as GPIO
import dht11
import firebase_admin
from firebase_admin import firestore
import pytz
import datetime
import time

def dht():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    dhtrst = dht11.DHT11(23).read()
    while dhtrst.temperature == 0 and dhtrst.humidity == 0:
        time.sleep(5)
        dhtrst = dht11.DHT11(23).read()
    return dhtrst 

firebase_admin.initialize_app()

db = firestore.client()
dhtrst = dht()

values = {
    "date" : datetime.datetime.now(pytz.timezone("Asia/Tokyo")),
    "Temp" : dhtrst.temperature,
    "Humidity" : dhtrst.humidity
}

#print(dt, dh, dbat)
db.collection("Room").add(values)