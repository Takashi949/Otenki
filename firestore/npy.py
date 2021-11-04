import firebase_admin
from firebase_admin import firestore
import subprocess
import datetime
import pytz
import sys
#import RPi.GPIO as GPIO

firebase_admin.initialize_app()

db = firestore.client()

def senddata():
    temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
    cusg = subprocess.check_output(["vcgencmd", "measure_clock", "arm"]).decode("utf-8")
    tld = subprocess.check_output(["vcgencmd", "get_throttled"]).decode("utf-8")
    tmp = subprocess.check_output(["vcgencmd", "read_ring_osc"]).decode("utf-8")
    osc = tmp[17:-24]
    tmp = subprocess.check_output(["vcgencmd", "mem_oom"]).decode("utf-8")
    i = tmp.find("events:")
    j = tmp.find("\n")
    mem = tmp[i+8:j]
    values = {
                'date':datetime.datetime.now(pytz.timezone("Asia/Tokyo")),
                'temp': float(temp[5:-3]),
                'cpu_usage': int(cusg[14:-1]),
                'BatteryStatus': tld[10:-1],
                'osc':float(osc),
                'mem':int(mem),
              }
    results = db.collection("Avai").document("avai").set(values)
    print(results)

senddata()