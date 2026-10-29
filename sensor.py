from machine import ADC
from time import sleep


class Sensor:
    def __init__(self, pin):
        self.pin = pin
        self.surface = 1

        self.reading_Pin = ADC(self.pin)
        
    def read(self):
            reading = self.reading_Pin.read_u16()
            print(reading)
            
    def read_cont(self, interval): #interval how many times a second
        while True:
            self.read()
            sleep(1/interval)
            
    def bin_read(self, switch, threshold):
        reading = self.reading_Pin.read_u16()
        if self.surface == 0 and reading > switch + threshold:
            self.surface = 1
        elif self.surface == 1 and reading < switch - threshold:
            self.surface = 0
        print(self.surface)    
        return self.surface
    
    def read_cont_bin(self, interval, switch, threshold):
        while True:
            self.bin_read(switch, threshold)
            sleep(1/interval)