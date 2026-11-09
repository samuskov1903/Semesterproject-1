from machine import ADC, Pin
from time import sleep, time
import _thread


class Sensor:
    def __init__(self, sensorpin, led=None):
        self.pin = sensorpin
        self.surface = 1 # Repræseter farven overfladen, 1 = hvid, 0 = Sort
        self.running = True
        self.logging = False
        self.log_thread_running = False
        self.sensor_LED = led
        self.sensor_LED_pin = Pin(self.sensor_LED, Pin.OUT) if self.sensor_LED is not None else None
        self.reading_Pin = ADC(self.pin) # Laver ADC af sensor Pin
        self.log_list = []
            
        
    def read(self):
            reading = self.reading_Pin.read_u16()
            return reading
        
    def light_led(self, status):
        if self.sensor_LED_pin is None:
            return
        if status == "on":
            self.sensor_LED_pin.on()
        else:
            self.sensor_LED_pin.off()
        
    def read_cont(self, interval): #interval how many times a second
        while self.running:
            self.read()
            sleep(1/interval)
            
    def bin_read(self, switch, threshold): # Switch er det punkt hvor at den skifter farve, threshold giver en buffer zone
        reading = self.reading_Pin.read_u16()
        if self.surface == 0 and reading > switch + threshold: # Hvis surface er 0 altså sort, og ADC værdien stiger over switch værdien og buffer zonen
            self.surface = 1 # Kalder overfladen tilbage på hvid
        elif self.surface == 1 and reading < switch - threshold: #Samme som over undtagen, her er det hvis ADC'en falder under switchværdien og buffer zonen
            self.surface = 0 # Kalder overfladen til sort
        print(self.surface)    # Printer det
        return self.surface 
    
    def read_cont_bin(self, interval, switch, threshold):
        while self.running:
            self.bin_read(switch, threshold)
            sleep(1/interval)
            
    def read_cont_bin_led(self, interval, switch, threshold): # Gør næsten det samme som koden over, undtagen den lyser LED'en, når overfladen er sort
        pin = Pin("LED", Pin.OUT)
        while self.running:
            self.bin_read(switch, threshold)
            if self.surface == 1:
                pin.on()
            elif self.surface == 0:
                pin.off()
            sleep(1/interval)
            
    def log_to_list(self, interval=100):
        while self.running and self.logging:
            self.log_list.append([time(), self.read()])
            sleep(1 / interval)
            
    def save_data(self, file_name, data):
        with open(file_name, "a") as log:
            log.write(data)
    
    def read_save_cont(self, file_name, interval):
        with open(file_name, "w"):
            pass
        while self.running:
                data = self.read()
                print(data)
                self.save_data(file_name, str(data) + "\n")
                sleep(1/interval)           
      
    def log_to_file(self, filename, direction, interval=10, batch_size=20):
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
        self.logging = True
        _thread.start_new_thread(
            self.log_to_file,
            (filename, direction, 15, 150),
        )

        robot.turn_on_point_robot_angle(180, direction, 0.01)

        self.logging = False
        while self.log_thread_running:
            sleep(0.01)
