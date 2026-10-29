from machine import ADC, Pin
from time import sleep


class Sensor:
    def __init__(self, pin):
        self.pin = pin
        self.surface = 1 # Repræseter farven overfladen, 1 = hvid, 0 = Sort
        self.running = True

        self.reading_Pin = ADC(self.pin) # Laver ADC af sensor Pin
        
    def read(self):
            reading = self.reading_Pin.read_u16() # Laver en reading af pin
            print(reading)
            
    def read_cont(self, interval): #interval how many times a second
        while self.running:
            self.read()
            sleep(1/interval)
            
    def bin_read(self, switch, threshold): # Switch er det punkt hvor at den skifter farve, threshold giver en buffer zone
        reading = self.reading_Pin.read_u16()
        if self.surface == 0 and reading > switch + threshold: # Hvis surface er 0 altså sort, og ADC værdien stiger over switch værdien og buffer zonen
            self.surface = 1 # Kalder overfladen tilbage på hvid
        elif self.surface == 1 and reading < switch - threshold: #Samme som over undtagen, her er det hvis ADC'en falder under switchværdien og buffer zonen
            self.surface = 0 # Kalder overfladen til sort
        print(self.surface)    # Printer det
        return self.surface 
    
    def read_cont_bin(self, interval, switch, threshold): # Funktionen her gør blot at sensoren bliver ved med at opsamle om der er sort eller hvidt underlag, med et hvis interval
        while True: 
            self.bin_read(switch, threshold)
            sleep(1/interval)
            
    def read_cont_bin_led(self, interval, switch, threshold): # Gør næsten det samme som koden over, undtagen den lyser LED'en, når overfladen er sort
        pin = Pin("LED", Pin.OUT)
        while True:
            self.bin_read(switch, threshold)
            if self.surface == 1:
                pin.on()
            elif self.surface == 0:
                pin.off()
            sleep(1/interval)