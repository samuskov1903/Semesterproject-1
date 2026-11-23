from connect import CarBle
from stepper_motor import StepperMotor
from Differential_drive import differentieldrive
import asyncio
from machine import Pin
from time import ticks_ms, ticks_diff
from time import sleep
from OldController import Controller

leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]

motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.2)
motorleft.set_step_mode("half")
motorright.set_step_mode("half")

robot = differentieldrive(motorleft, motorright, 8.6, 24.5)

button = Pin("GP18", Pin.IN, Pin.PULL_DOWN)
button_power = Pin("GP19", Pin.OUT)
button_power.value(1)

running = True
last_press_ms = 0


def button_pressed(pin):
    global running, last_press_ms

    now = ticks_ms()
    if pin.value() == 1 and ticks_diff(now, last_press_ms) > 100:
        last_press_ms = now
        running = False
        robot.stop()
        print("STOP")


button.irq(trigger=Pin.IRQ_RISING, handler=button_pressed)


async def handle_message(message):
    if not running:
        robot.stop()
        return

    try:
        text = message.decode().strip().strip("[]")
        turn, speed = map(float, text.split(","))
    except (UnicodeError, ValueError, IndexError, AttributeError):
        return

    if turn < -0.1:
        robot.turn_on_point_robot_angle(1, "right", 0.01)
    elif turn > 0.1:
        robot.turn_on_point_robot_angle(1, "left", 0.01)
    elif speed < -0.1:
        if speed < -0.6:
            robot.move_dist(1, "backward", 0.005)
        elif speed < -0.1:
            robot.move_dist(1, "backward", 0.01)
    elif speed > 0.1:
        if speed > 0.6:
            robot.move_dist(1, "forward", 0.005)
        elif speed > 0.1:
            robot.move_dist(1, "forward", 0.01)
        
        


async def main():
    while running:
        car = CarBle()
        try:
            print("Searching...")
            await car.FindController()
            print("Connected")
            await car.listen(handle_message)
        except Exception as error:
            print("BLE error:", error)

        if car.connection is not None:
            try:
                await car.connection.disconnect()
            except Exception:
                pass

        await asyncio.sleep(1)

    robot.stop()
    print("Stopped and disconnected")


asyncio.run(main())