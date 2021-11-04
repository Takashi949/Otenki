import firebase_admin
from firebase_admin import firestore
import subprocess
import datetime
import pytz
import sys

firebase_admin.initialize_app()

db = firestore.client()

def senddata():
    values = {'msg': "boot", 'date':datetime.datetime.now(pytz.timezone("Asia/Tokyo"))}
    results = db.collection("Extra").add(values)

senddata()