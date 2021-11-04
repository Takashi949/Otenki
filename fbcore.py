import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import datetime


# Use a service account
cred = credentials.Certificate('../serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

with open("./rpimonitor-export(1).json", mode='r') as f:
   data = json.load(f)

for l in data["Ame"].values():
   u = {
       u'date':datetime.datetime.fromisoformat(l["date"]),
       u'BatteryStatus':l["Battery"],
       u'Humidity':l["Humidity"],
       u'Temp':l["Temp"]
   }
   #print(u)
   db.collection(u'Ame').add(u)