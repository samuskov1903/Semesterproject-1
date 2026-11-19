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
    try:
        text = message.decode()
        text = text.strip().strip("[]")
        parts = text.split(",")
        turn = float(parts[0])
        speed = float(parts[1])
    except (UnicodeError, ValueError, IndexError, AttributeError):
        return

    print("Controller values:", turn, speed)

    if turn < 0.1:
        print("Hello")
        robot.turn_on_point_robot_steps(1, "left", 0.01)
    elif turn > 0.1:
        print("fuck off")
        robot.turn_on_point_robot_steps(1, "right", 0.01)
    else:
        print("im stupid")
        
    if speed < 0.1:
        print("back")
        robot.move_dist(1, "backward", 0.01)
    elif speed > 0.1:
        print("forward")
        robot.move_dist(1, "forward", 0.01)
    else:
        print("im dum")


async def main():
    while True:
        car = CarBle()
        try:
            print("Searching for controller Pico...")
            await car.FindController()
            print("Connected to controller Pico")
            await car.listen(handle_message)
        except Exception as error:
            print("BLE error:", error)
        await asyncio.sleep(1)


asyncio.run(main())