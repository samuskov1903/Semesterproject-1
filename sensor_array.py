from sensor import Sensor

class sensor_array:
    def __init__(self, sensor_pins=[],led_pins=[]):
        self.sensors =[Sensor(pin) for pin in sensor_pins]

            
    def read(self):
        return [sensor.read() for sensor in self.sensors]

    def read_bin(self, switch, threshold):
        return [
            sensor.bin_read(switch, threshold)
            for sensor in self.sensors
        ]