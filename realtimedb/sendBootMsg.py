import subprocess
import datetime
import pytz
import sys
import firebase_admin
from firebase_admin import db

firebase_admin.initialize_app()

def senddata():
    values = {'msg': "boot", 'date':datetime.datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()}
    results = db.child("Extra").push(values)

senddata()