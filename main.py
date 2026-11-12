from time import sleep
from sensor import Sensor
from Differential_drive import differentieldrive
from stepper_motor import StepperMotor


sensor1_pin = 28
sensor1_led_pin = 27
sensor2_pin = 26
sensor2_led_pin = 22
leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]
wheel_diameter = 8.6
wheel_base = 24.5
log_file = "turns.txt"


ldrleft = Sensor(sensor1_pin, sensor1_led_pin)
ldrleft.light_led("on")
ldrright = Sensor(sensor2_pin, sensor2_led_pin)
ldrright.light_led("on")



motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.2)
motorleft.set_step_mode("full")
motorright.set_step_mode("full")


robot = differentieldrive(
    motorleft,
    motorright,
    wheel_diameter,
    wheel_base,
)

#robot.move_dist(200, "forward", 0.001)

sleep(2)
while True:
    if ldrright.bin_read(30000, 2000) == 0:
        robot.turn_on_point_robot_angle(20, "left", 0.001)
    elif ldrleft.bin_read(30000, 2000) == 0:
        robot.turn_on_point_robot_angle(20, "right", 0.001)
    robot.move_dist(2, "forward", 0.001)

