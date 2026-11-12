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



motorleftfull = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorrightfull = StepperMotor(rightmotor_pins, pwm_pct=0.2)
motorleftmicro = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorrightmicro = StepperMotor(rightmotor_pins, pwm_pct=0.2)
motorleftfull.set_step_mode("full")
motorrightfull.set_step_mode("full")
motorleftmicro.set_step_mode(4)
motorrightmicro.set_step_mode(4)



robotfull = differentieldrive(
    motorleftfull,
    motorrightfull,
    wheel_diameter,
    wheel_base,
)
robotmicro = differentieldrive(motorleftmicro, motorrightmicro, wheel_diameter, wheel_base)

#robot.move_dist(200, "forward", 0.001)

sleep(2)
#robot.turn_curve_cm(2, "right", 0.005, 5)
#while True:
#    robotfull.move_dist(2,"forward", 0.00099999999)
#robot.move_dist(5, "forward", 0.001)

while True:
    if ldrright.bin_read(30000, 2000) == 0:
        robotmicro.turn_curve_cm(3, "right", 0.001, 3)
    elif ldrleft.bin_read(30000, 2000) == 0:
        robotmicro.turn_curve_cm(3, "left", 0.001, 3)
    robotfull.move_dist(1, "forward",0.002 )
