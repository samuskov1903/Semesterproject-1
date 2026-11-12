from time import sleep
from sensor import Sensor
from Differential_drive import differentieldrive
from stepper_motor import StepperMotor


sensor_pin = 28
sensor_led_pin = 27
leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]
wheel_diameter = 8.6
wheel_base = 24.5
log_file = "turns.txt"


ldr = Sensor(sensor_pin, sensor_led_pin)
ldr.light_led("on")

potentiometer_pin = 26
potentiometer = Sensor(potentiometer_pin)

motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.2)
motorleft.set_step_mode("half")
motorright.set_step_mode("half")


robot = differentieldrive(
    motorleft,
    motorright,
    wheel_diameter,
    wheel_base,
)

delays = [0.25, 0.166, 0.111, 0.074, 0.049, 0.033, 0.022, 0.014, 0.001]

def speed_control(raw_val):
    raw_val = max(0, min(65535, raw_val))
    zone_størrelse = 65535 / 19
    zone_indeks = int(raw_val / zone_størrelse)
    if zone_indeks > 18:
        zone_indeks = 18

    trin = zone_indeks - 9

    if trin == 0:
        return "stop", 0
    elif trin > 0:
        indeks = trin - 1
        return "forward", delays[indeks]
    else:
        indeks = abs(trin) - 1
        return "backwards", delays[indeks]


try:
    while True:
        raw_val = potentiometer.read()
        retning, nyt_delay = speed_control(raw_val)
        if retning == "stop":
            robot.stop()

        elif retning == "forward":
            motorleft.delay = nyt_delay
            motorright.delay = nyt_delay

        elif retning == "backwards":
            motorleft.delay = nyt_delay
            motorright.delay = nyt_delay

        sleep(0.05)
except KeyboardInterrupt:
    robot.stop()
          



try:
    with open(log_file, "w") as log:
        log.write("Sensor recordings\n")

    sleep(1)
    ldr.record_turn(robot, "left", log_file)

    sleep(1)
    ldr.record_turn(robot, "right", log_file)
finally:
    ldr.light_led("off")
    ldr.logging = False
    ldr.running = False
    robot.stop()
    
