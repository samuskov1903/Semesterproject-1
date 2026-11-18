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
    turn_ratio = turn/1000
    if movementList[0] != 0:
        if turn < 0:
            robot.turn_curve_cm(1, "left", speed, turn_ratio)

        elif turn > 0:
            robot.turn_curve_cm(1, "right", speed, turn_ratio)
        
        else:
            if speed < 0:
                robot.move_dist(1, "backward", speed)
            elif speed > 0:
                robot.move_dist(1, "forward", speed)