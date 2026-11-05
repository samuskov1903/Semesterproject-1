from time import sleep
from sensor import Sensor
from Differential_drive import differentieldrive
from stepper_motor import StepperMotor


sensor_pin = 28
leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]
wheel_diameter = 8.6
wheel_base = 24.5
log_file = "turns.txt"


ldr = Sensor(sensor_pin)

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


try:
    with open(log_file, "w") as log:
        log.write("Sensor recordings\n")

    sleep(1)
    ldr.record_turn(robot, "left", log_file)

    sleep(1)
    ldr.record_turn(robot, "right", log_file)
finally:
    ldr.logging = False
    ldr.running = False
    robot.stop()
