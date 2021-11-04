import sys
from gattlib import GATTRequester
import struct
import binascii
import time
#古い方のesp32 30:AE:A4:9C:2F:9E
#新しい方のesp32 4C:11:AE:EB:91:86
old_esp32_mac="30:AE:A4:9C:2F:9E"
new_esp32_mac="4C:11:AE:EB:91:86"
class Reader(object):
    def __init__(self, address):
        try:
            self.requester = GATTRequester(address, True)
        except:
            print("error")
            exit(1)
        #self.connect()

    def connect(self):
        self.requester.connect(True)

    def request_data(self):
        self.data = self.requester.read_by_uuid("beb5483e-36e1-4688-b7f5-ea07361b26a9")[0]
        s = self.data[0:4]
        d = self.data[4:8]
        k = self.data[8:12]
        dtemp = struct.unpack('<f', binascii.unhexlify(str(s.hex())))[0]
        dhum = struct.unpack('<f', binascii.unhexlify(str(d.hex())))[0]
        dbat = struct.unpack('<f', binascii.unhexlify(str(k.hex())))[0]

        return dtemp, dhum, dbat


if __name__ == '__main__':
    print(Reader(new_esp32_mac).request_data())
    
