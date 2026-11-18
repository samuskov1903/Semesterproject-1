import asyncio
from Connect import ControlBLE
from sensor import Sensor


controller = ControlBLE()

joystick_y_pin = 28
joystick_y = Sensor(joystick_y_pin)
joystick_x_pin = 26
joystick_x = Sensor(joystick_x_pin)

controller.advertise()

while True:
    #hussein kode
    message= [joystick_x.read(), joystick_y.read()]
    
    
    #skal sende en liste af de to potentiometer
    controller.send(message)