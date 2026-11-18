from connect import CarBle
from stepper_motor import StepperMotor
from Differential_drive import differentieldrive
import asyncio

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


async def handle_message(message):
    print("Controller message:", message)
    try:
        parts = message.decode().strip("[]").split(",")
        turn = int(parts[0])
        speed = int(parts[1])
    except (ValueError, IndexError, AttributeError):
        return

    turn_ratio = turn / 1000
    if turn < 0:
        robot.turn_curve_cm(1, "left", speed, turn_ratio)
    elif turn > 0:
        robot.turn_curve_cm(1, "right", speed, turn_ratio)
    elif speed < 0:
        robot.move_dist(1, "backward", speed)
    elif speed > 0:
        robot.move_dist(1, "forward", speed)


async def main():
    car = CarBle()
    await car.FindController()
    await car.listen(handle_message)


asyncio.run(main())