from machine import ADC
from time import sleep


class Sensor:
    def __init__(self, pin):
        self.pin = pin

        self.reading_Pin = ADC(self.pin)
        
    def read(self):
            reading = self.reading_Pin.read_u16()
            print(reading)
            
    def read_cont(self, interval): #interval how many times a second
        while True:
            self.read
            sleep(1/interval)