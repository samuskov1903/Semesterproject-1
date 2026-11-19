from machine import Pin, ADC
from time import sleep_us


class Multiplexer_data:
    """Run through the selected multiplexer outputs"""

    def __init__(self, sensor_count=6, SelectorPins=[27,26,22],read_pin=28,Activated_Pins=[18,19]):
        self.s_pins = [Pin(i,Pin.OUT) for i in SelectorPins]
        self.sensor_count=sensor_count
        self.sensor_pin = ADC(read_pin)
        self.sensor_data=[]
        self.activated_pins=[Pin(i,Pin.OUT) for i in Activated_Pins]
        for i in self.activated_pins:
            i.value(1)

    def select_pinners(self, p, pins): #function for selecting "p"th output in the multiplexer (remember to count from zero)
        bin_output = '{0:03b}'.format(p) #converting the output number to binary for multiplex select
        for i in range(3): #binary 7 is 3 digits (1 1 1)
            pins[i].value(int(list(bin_output)[i])) #first pin sets value as first number, second pin sets value as second number....

    def scan_all_sensors(self): #function collecting data from all sensors, returning as list
        sensor_data=[] #clear list, ready for data
        for i in range(self.sensor_count): #repeat for every sensor
            self.select_pinners(i,self.s_pins)
            sleep_us(20) #buffer time to allow pico to send signal to multiplex, and multiplex to switch output
            sensor_data.append(self.sensor_pin.read_u16()) #append sensor data, n'th sensor outputs to n'th slot in list
        return sensor_data #returns list of all data ready for processing

