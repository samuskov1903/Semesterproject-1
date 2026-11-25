from machine import ADC, Pin


class Sensor:
    """Read an analogue sensor and optionally control its LED."""

    def __init__(self, sensorpin, led=None):
        self.sensor_led = Pin(led, Pin.OUT) if led is not None else None
        self.reading_pin = ADC(sensorpin)

    def read(self):
        """Return the current analogue reading as a 16-bit value."""
        return self.reading_pin.read_u16()

    def light_led(self, status):
        """Turn the optional sensor LED on or off."""
        if self.sensor_led is not None:
            if status == "on":
                self.sensor_led.on()
            else:
                self.sensor_led.off()
