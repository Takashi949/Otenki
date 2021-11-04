import sys
import firebase_admin
from firebase_admin import db
import pytz
import datetime
sys.path.append('../')
import blegttt

firebase_admin.initialize_app()

ble = blegttt.Reader("30:AE:A4:9C:2F:9E")
dt, dh, dbat = ble.request_data()

values = {
    "date" : datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat(),
    "Temp" : dt,
    "Humidity" : dh,
    "Battery"  : dbat
}

print(dt, dh, dbat)
db.child("Ame").push(values)