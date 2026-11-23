from connect import CarBle
from stepper_motor import StepperMotor
from Differential_drive import differentieldrive
import asyncio

# GPIO pins used by the left and right stepper motor drivers.
leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]

# Physical robot measurements in centimetres.
wheel_diameter = 8.6
wheel_base = 24.5

# Create both stepper motors and set them to half-step mode.
motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.2)
motorleft.set_step_mode("half")
motorright.set_step_mode("half")

# Combine the motors into a differential-drive robot.
robot = differentieldrive(
    motorleft,
    motorright,
    wheel_diameter,
    wheel_base,
)


async def handle_message(message):
    # Convert the BLE notification into two floating-point joystick values.
    try:
        text = message.decode()
        text = text.strip().strip("[]")
        parts = text.split(",")
        turn = float(parts[0])
        speed = float(parts[1])
    except (UnicodeError, ValueError, IndexError, AttributeError):
        # Ignore notifications that do not contain valid controller data.
        return

    print("Controller values:", turn, speed)

    # Turn left or right from the horizontal joystick value.
    # Values around zero are also treated as commands by the current thresholds.
    if turn < 0.1:
        robot.turn_on_point_robot_steps(1, "left", 0.01)
    elif turn > -0.1:
        robot.turn_on_point_robot_steps(1, "right", 0.01)

    # Move forward or backward from the vertical joystick value.
    # The distance is fixed at 1 cm for each received notification.
    if speed < 0.1:
        robot.move_dist(1, "backward", 0.01)
    elif speed > 0.1:
        robot.move_dist(1, "forward", 0.01)

    print(f"Turn: {turn:.2f}, Speed: {speed:.2f}")


async def main():
    # Keep trying to reconnect until a controller Pico is found.
    while True:
        car = CarBle()
        try:
            print("Searching for controller Pico...")
            await car.FindController()
            print("Connected to controller Pico")
            # Wait for BLE notifications and send each one to handle_message().
            await car.listen(handle_message)
        except Exception as error:
            print("BLE error:", error)
        # Pause before creating a new connection attempt.
        await asyncio.sleep(1)


asyncio.run(main())