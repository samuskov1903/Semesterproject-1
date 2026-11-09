from machine import ADC, Pin
from time import sleep, time
import _thread


class Sensor:
    """Read an analogue surface sensor and optionally control its LED."""

    def __init__(self, sensorpin, led=None):
        # Store the ADC input pin and the optional LED output pin.
        self.pin = sensorpin
        self.surface = 1  # Surface state: 1 means white and 0 means black.
        self.running = True  # Background reading/logging loops run while True.
        self.logging = False  # Enables or disables the file logging loop.
        self.log_thread_running = False  # Indicates whether the logging thread is active.
        self.sensor_LED = led
        self.sensor_LED_pin = Pin(self.sensor_LED, Pin.OUT) if self.sensor_LED is not None else None
        self.reading_Pin = ADC(self.pin)  # Convert the sensor pin into an ADC input.
        self.log_list = []
            
        
    def read(self):
        """Return the current analogue reading as a 16-bit value."""
        reading = self.reading_Pin.read_u16()
        return reading
        
    def light_led(self, status):
        """Turn the optional sensor LED on or off."""
        if self.sensor_LED_pin is None:
            return
        if status == "on":
            self.sensor_LED_pin.on()
        else:
            self.sensor_LED_pin.off()
        
    def read_cont(self, interval):
        """Continuously read the sensor at the requested samples per second."""
        while self.running:
            self.read()
            sleep(1/interval)
            
    def bin_read(self, switch, threshold):
        """Convert the analogue reading to a stable black/white state.

        The threshold creates a dead zone so small fluctuations do not
        repeatedly switch the detected surface.
        """
        reading = self.reading_Pin.read_u16()
        if self.surface == 0 and reading > switch + threshold:
            self.surface = 1  # The reading moved above the white-surface limit.
        elif self.surface == 1 and reading < switch - threshold:
            self.surface = 0  # The reading moved below the black-surface limit.
        print(self.surface)
        return self.surface
    
    def read_cont_bin(self, interval, switch, threshold):
        """Continuously update the binary surface state."""
        while self.running:
            self.bin_read(switch, threshold)
            sleep(1/interval)
            
    def read_cont_bin_led(self, interval, switch, threshold):
        """Update the binary state continuously and mirror it on the board LED."""
        pin = Pin("LED", Pin.OUT)
        while self.running:
            self.bin_read(switch, threshold)
            if self.surface == 1:
                pin.on()
            elif self.surface == 0:
                pin.off()
            sleep(1/interval)
            
    def log_to_list(self, interval=100):
        """Store timestamped readings in memory at the requested rate."""
        while self.running and self.logging:
            self.log_list.append([time(), self.read()])
            sleep(1 / interval)
            
    def save_data(self, file_name, data):
        """Append text data to a file."""
        with open(file_name, "a") as log:
            log.write(data)
    
    def read_save_cont(self, file_name, interval):
        """Continuously read the sensor and append each reading to a file."""
        with open(file_name, "w"):
            pass
        while self.running:
            data = self.read()
            print(data)
            self.save_data(file_name, str(data) + "\n")
            sleep(1/interval)
      
    def log_to_file(self, filename, direction, interval=10, batch_size=20):
        """Log timestamped readings to a file in batches.

        Batching reduces how often the file is written while preserving the
        final partial batch when logging stops.
        """
        self.log_thread_running = True
        buffer = []

        try:
            with open(filename, "a") as log:
                log.write("\n--- " + direction + " turn ---\n"+"sample rate:" + str(interval) +"\n")

                while self.running and self.logging:
                    buffer.append(str(time()) + "," + str(self.read()))
                    if len(buffer) >= batch_size:
                        log.write("\n".join(buffer) + "\n")
                        log.flush()
                        buffer.clear()

                    sleep(1 / interval)

                if buffer:
                    log.write("\n".join(buffer) + "\n")
                    log.flush()
        finally:
            self.log_thread_running = False
        
    def record_turn(self, robot, direction, filename):
        """Log one turn while the robot performs the requested movement."""
        self.logging = True
        _thread.start_new_thread(
            self.log_to_file,
            (filename, direction, 15, 150),
        )

        robot.turn_on_point_robot_angle(180, direction, 0.01)

        # Stop collecting readings and wait until the logging thread finishes
        # writing its remaining buffered data.
        self.logging = False
        while self.log_thread_running:
            sleep(0.01)
s
