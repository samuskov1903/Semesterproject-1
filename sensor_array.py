from machine import Pin, ADC
from sensor import Sensor
from led import LED

class SensorArray:
    def __init__(self, select_pins, z_pin, sensor_pins=[],led_pins=[]):
        self.sensors =[Sensor(pin) for pin in sensor_pins]
        self.leds = [LED(pin) for pin in led_pins]
        self.sensor_pins = sensor_pins
        self.select_pin = select_pins
        self.s_pins = [Pin(i,Pin.OUT) for i in self.select_pin]
        self.z_pin = ADC(z_pin)
            
    def read(self):
        return [sensor.read() for sensor in self.sensors]

    def read_bin(self, switch, threshold):
        return [
            sensor.bin_read(switch, threshold)
            for sensor in self.sensors
        ]
        
    def led_status(self, status):
        for led in self.leds:
            if status == "on":
                led.on()
            else:
                led.off()

    def select_pin(p, pins):
        for i in range (3):
            pins[i].value((p>>i)&1)
            print(pins[i].value((p>>i)&1))

    def read_sens():
        sens = []
        for i in range(8):
            self.select_pin(i, self.s_pins)
            sens.append(self.z_pin.read_u16())
        return sens
            