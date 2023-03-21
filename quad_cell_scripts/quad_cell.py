import serial
import csv
import datetime
import struct
import time
import numpy as np
HEADER = b'87'
DEBUG = False

# sample index, ch1, ch2, ch3, ch4
PAYLOAD_FORMAT = 'IIIIIiiiiiiiiIIIIII'
PAYLOAD_SIZE = struct.calcsize(PAYLOAD_FORMAT)
FILE_NAME_PREFIX = 'quadcell_raw_samples'
CSV_FIRST_LINE = ['sample index','ch1','ch2','ch3','ch4','ch1I','ch1Q','ch2I','ch2Q','ch3I','ch3Q','ch4I','ch4Q','ch0cicI','ch0cicQ','ch1cicI','ch1cicQ','ch2cicI','ch2cicQ']


class Decoder:
    def __init__(self) -> None:
        self.buffer = b''
        self.in_sync = False
        self.header_good = False

    def add(self, data):
        self.buffer += data

    def check_header(self):
        correct = False
        if len(self.buffer) > 1:
            if self.buffer[:2] == HEADER:
                self.buffer = self.buffer[2:]
                correct = True
                if not self.in_sync: print('Decoder synchronized')
                self.in_sync = True
            else:
                if self.in_sync: print('Lost synchronization')
                self.buffer = self.buffer[1:]
                self.in_sync = False
                if DEBUG: print('Incorect header, got %s' % self.buffer[:2])
        return correct

    def get_payload(self):
        if len(self.buffer) >= PAYLOAD_SIZE:
            res = struct.unpack(PAYLOAD_FORMAT, self.buffer[:PAYLOAD_SIZE])
            self.buffer = self.buffer[PAYLOAD_SIZE:]
            return res
        else: return None

    def get_values(self):
        if not self.header_good:
            self.header_good = self.check_header()
        if self.header_good:
            res = self.get_payload()
            if res:
                self.header_good = False
                return res
        return None
def main():
    with \
        serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1.0) as ser, \
        open('quadcell_samples/%s_%s' % (FILE_NAME_PREFIX, datetime.datetime.utcnow()),'w') as csv_file:

        decode = Decoder()
        csv_o = csv.writer(csv_file)
        csv_o.writerow(CSV_FIRST_LINE)

        print('Header: '+'-'.join(['%02X' % x for x in HEADER]))

        total_samples = 0
        samples_this_second = 0
        next_second = time.time() + 1
        sums = [0,0,0,0]

        def signed18(x):
            if (x >> 17) & 1:
                #x + 0xFFFC0000
                #x = struct.unpack('i',struct.pack('I',x))[0]
                x = x - 0x3FFFF
            return x
                
        output = []
        while 1:
            data = ser.read(size = PAYLOAD_SIZE+len(HEADER))
            decode.add(data)
            res = decode.get_values()
            if res:
                if DEBUG: print(hex(res[0]),res[1:])
                
                csv_o.writerow(list(res[:(len(PAYLOAD_FORMAT)-6)]) + [signed18(x) for x in res[(len(PAYLOAD_FORMAT)-6):]])
                total_samples += 1
                samples_this_second += 1
                sums = [a+b for a,b in zip(res[1:],sums)]
            if time.time() > next_second:
                next_second += 1
                print('%d sample/sec, %d total' % (samples_this_second, total_samples))
                print([a/max(samples_this_second,1) for a in sums])
                output =  [a/max(samples_this_second,1) for a in sums]
                std = np.std(np.array(sums))
                break
    return output,std
        
    
                #samples_this_second = 0
                #sums = [0,0,0,0]
        