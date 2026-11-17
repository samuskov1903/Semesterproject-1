from machine import Pin
from time import sleep

selectPin = [12,11,10] #pins connected to S1 S2 S3 on multiplex
s_pins = [Pin(i,Pin.OUT) for i in selectPin] 
led_pin = Pin(20,Pin.OUT) #signal pin (demo used LED)
led_pin.value(1)

"""
RENAME FILE TO "main.py"
"""


def select_pinners(p, pins): #function for selecting "p"th output in the multiplexer
    bin_output = '{0:03b}'.format(p) #converting the output number to binary for multiplex select
    for i in range(3): #binary 7 is 3 digits (1 1 1)
        pins[i].value(int(list(bin_output)[i])) #first pin sets value as first number, second pin sets value as second number....


for i in range(4):
    select_pinners(i, s_pins)
    sleep(1)
