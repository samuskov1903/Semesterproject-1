#Hussein Mohamed Kleit   hukle26@student.sdu.dk

from time import sleep
from stepper_motor import StepperMotor
from Differential_drive import differentieldrive

led_pins = [16, 17, 18, 19]

leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]

motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.4)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.4)

motorleft.set_step_mode("half") # "full" for full step. "half" for half step og et nummer uden "" for micro
motorright.set_step_mode("half") # "full" for full step. "half" for half step og et nummer uden "" for micro

robot = differentieldrive(motorleft, motorright, 8.6)

sleep(2)
for i in range(4):
    robot.move_dist(10,"forward", 0.02)
    sleep(1)
    robot.turn_on_point_robot_angle(90, "left", 0.02)
    sleep(1)
