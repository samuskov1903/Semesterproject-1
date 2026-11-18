import asyncio
from Connect import ControlBLE


controller = ControlBLE()

controller.advertise()

while True:
    #hussein kode
    
    #skal sende en liste af de to potentiometer
    controller.send()