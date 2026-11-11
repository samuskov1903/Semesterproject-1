from machine import Pin

class LED:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)

    def on(self):
        self.pin.on()

    def off(self):
        self.pin.off()