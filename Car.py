import asyncio

from Connect import CarBle
from stepper_motor import StepperMotor
from Differential_drive import differentieldrive

leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]
wheel_diameter = 8.6
wheel_base = 24.5

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


car = CarBle()

car.FindController()


while True:
    movementList = car.listen()
    turn = movementList[0]
    speed = movementList[1]
    if movementList[0] != 0:
        if turn < 0:
            
