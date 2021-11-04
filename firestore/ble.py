import firebase_admin
from firebase_admin import firestore
import pytz
import datetime
import blegttt

#古い方のesp32 30:AE:A4:9C:2F:9E
#新しい方のesp32 4C:11:AE:EB:91:86
old_esp32_mac="30:AE:A4:9C:2F:9E"
new_esp32_mac="4C:11:AE:EB:91:86"

firebase_admin.initialize_app()

db = firestore.client()
ble = blegttt.Reader(new_esp32_mac)
dt, dh, dbat = ble.request_data()

values = {
    "date" : datetime.datetime.now(pytz.timezone("Asia/Tokyo")),
    "Temp" : dt,
    "Humidity" : dh,
    "Battery"  : dbat
}

print(dt, dh, dbat)
db.collection("Ame").add(values)