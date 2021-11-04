#!/bin/sh
BLE_WORK_COUNT=0
sudo python3 /home/pi/Otenki/firestore/ble.py
while [ ! "$?" -eq 0 ]
do
   BLE_WORK_COUNT=`expr $BLE_WORK_COUNT + 1`
   if [ BLE_WORK_COUNT -eq 10]
   then
      exit 1
   fi
   sleep 3
   sudo python3 /home/pi/Otenki/firestore/ble.py
done