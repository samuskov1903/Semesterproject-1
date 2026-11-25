from connect import CarBle
from stepper_motor import StepperMotor
from Differential_drive import differentieldrive
import asyncio
from machine import Pin
from time import ticks_ms, ticks_diff


# Configure the motor-driver pins and select half-step movement.
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

# Assign indicator LEDs and switch them off during startup.
backwards_led = Pin("GP9", Pin.OUT)
lav_fart_led = Pin("GP10", Pin.OUT)
høj_fart_led = Pin("GP11", Pin.OUT)
venstre_drej_led = Pin("GP12", Pin.OUT)
højre_drej_led = Pin("GP13", Pin.OUT)

alle_leds = [lav_fart_led, høj_fart_led, venstre_drej_led, højre_drej_led, backwards_led]

for led in alle_leds:
    led.value(0)  # Sluk alle LED'er ved opstart

def led_status(turn, speed):
    """Display the current steering direction and speed."""
    # Sluk alle LED'er først
    for led in alle_leds:
        led.value(0)

    # Tænd de relevante LED'er baseret på turn og speed værdierne
    if turn > 0.1:
        højre_drej_led.value(1)
    elif turn < -0.1:
        venstre_drej_led.value(1)

    if speed < -0.6:
        backwards_led.value(1)
        høj_fart_led.value(1)
    elif speed < -0.1:
        backwards_led.value(1)
        lav_fart_led.value(1)
    elif speed > 0.1:
        if speed > 0.6:
            høj_fart_led.value(1)
        elif speed > 0.1:
            lav_fart_led.value(1)

running = True
last_press_ms = 0


def button_pressed(pin):
    """Stop the robot when pressed, filtering out button bounce."""
    global running, last_press_ms
    now = ticks_ms()
    if pin.value() == 1 and ticks_diff(now, last_press_ms) > 200:
        last_press_ms = now
        if running:
            running = False
            robot.emergency_stop()
            print("STOP")
        else:
            running = True
            robot.running = True
            print("Running again")

button.irq(trigger=Pin.IRQ_RISING, handler=button_pressed)


async def handle_message(message):
    """Decode a [turn, speed] command and move the robot."""
    try:
        text = message.decode().strip().strip("[]")
        turn, speed = map(float, text.split(","))
    except (UnicodeError, ValueError, IndexError, AttributeError):
        return

    # Give steering priority if the controller sends both axes at once.
    if turn < -0.1:
        robot.turn_on_point_robot_angle(1, "right", 0.01)
    elif turn > 0.1:
        robot.turn_on_point_robot_angle(1, "left", 0.01)
    elif speed < -0.1:
        if speed < -0.6:
            robot.move_dist(1, "backward", 0.002)
        else:
            robot.move_dist(1, "backward", 0.02)
    elif speed > 0.1:
        if speed > 0.6:
            robot.move_dist(1, "forward", 0.002)
        else:
            robot.move_dist(1, "forward", 0.02)
    led_status(turn, speed)
async def main():
    """Keep the BLE link active and disconnect safely when stopped."""
    car = None

    async def disconnect_on_stop():
        # BLE disconnection must run in the event loop, not in the button IRQ.
        while True:
            if not running:
                if car is not None and car.connection is not None:
                    try:
                        if car.connection.is_connected():
                            await car.connection.disconnect()
                            print("BLE disconnected")
                    except Exception as error:
                        print("BLE disconnect error:", error)
                robot.stop()
                while not running:
                    await asyncio.sleep_ms(50)
            await asyncio.sleep_ms(50)

    asyncio.create_task(disconnect_on_stop())

    # Keep waiting while stopped so another button press can resume the car.
    while True:
        while not running:
            await asyncio.sleep_ms(50)

        # Scan for the controller and listen until stopped or disconnected.
        while running:
            car = CarBle()
            try:
                print("Searching...")
                await car.FindController()
                if not running:
                    if car.connection is not None and car.connection.is_connected():
                        await car.connection.disconnect()
                    break
                print("Connected")
                await car.listen(handle_message)
            except Exception as error:
                print("BLE error:", error)

            if not running:
                break

            await asyncio.sleep(1)

        robot.stop()
        print("Stopped and disconnected")
        while not running:
            await asyncio.sleep_ms(50)

asyncio.run(main())