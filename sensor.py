from machine import ADC
from time import sleep


class sensors:
    def __init__(self, pin):
        self.pin = pin

        self.reading_Pin = ADC(self.pin)
        
    def reading(self, interval): #interval how many times a second
        while True:
    
            reading = self.reading_Pin.read_u16()
            sleep(1/interval)
            print(reading)