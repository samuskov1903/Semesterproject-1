from machine import Pin, ADC
from time import sleep

selectPin = [4,5,6]
s_pins = [Pin(i,Pin.OUT) for i in selectPin]
z_pin = ADC(27)

def select_pin(p, pins):
    for i in range (3):
        pins[i].value((p>>i)&1)
        print(pins[i].value((p>>i)&1))

def read_sens():
    sens = []
    for i in range(8):
        select_pin(i, s_pins)
        sens.append(z_pin.read_u16())
    return sens

    


