
import serial
import numpy as np


class Sensor:
    def __init__(self, port = '/dev/tty0', freq = 15200, timeout = 3):
        self.port = port
        self.freq = freq
        self.timeout = timeout
        print('------------------------------ device initializing ------------------------------')
        self.device = serial.Serial( port, freq, timeout = timeout)
        print('device {} is on {} with frequency {} Hz.'.format(self.device.name, self.device.port, self.device.baudrate))
        print('------------------------------ device initialized -------------------------------')
        self.data = None
        self.flush()
    def read(self):
        # return ( type : np.array, shape: (16,1))
        # meaning A G M Q YPR define in opt
        while not self._read():
            pass
        data = np.array(self.data).reshape(16,1)
        return data

    def _read(self):
        string = self.device.readline()
        if string[0] != 'A':
            return False
        else:
            self.data = []
            string = string.strip()
            #print(string)
            for part in string.split('|'):
                #print(part)
                for value in part.split(' ')[1:]:
                    self.data.append(float(value))
            return True

    def flush(self):
        self.device.flushInput()
        

if __name__ == '__main__':
    sensor = Sensor("/dev/cu.usbmodem1413", 921600)
    while True:
        data = sensor.read()
        print(data)
